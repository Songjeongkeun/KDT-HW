"""Train and evaluate an LSTM for next sleep-stage prediction."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pyedflib
import torch
from PIL import Image, ImageDraw, ImageFont
from torch import nn
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler


STAGES = ["W", "N1", "N2", "N3", "REM"]
STAGE_TO_ID = {stage: index for index, stage in enumerate(STAGES)}
ANNOTATION_MAP = {
    "Sleep stage W": "W",
    "Sleep stage 1": "N1",
    "Sleep stage 2": "N2",
    "Sleep stage 3": "N3",
    "Sleep stage 4": "N3",
    "Sleep stage R": "REM",
}


@dataclass
class SplitData:
    x: np.ndarray
    y: np.ndarray
    subjects: np.ndarray


class SequenceDataset(Dataset):
    def __init__(self, data: SplitData) -> None:
        self.x = torch.as_tensor(data.x, dtype=torch.long)
        self.y = torch.as_tensor(data.y, dtype=torch.long)

    def __len__(self) -> int:
        return len(self.y)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.x[index], self.y[index]


class SleepStageLSTM(nn.Module):
    def __init__(
        self,
        hidden_size: int,
        num_layers: int,
        dropout: float,
        forget_gate_bias: float = 1.0,
    ) -> None:
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=len(STAGES),
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self._initialize_forget_gate_bias(forget_gate_bias)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(hidden_size, len(STAGES))

    def _initialize_forget_gate_bias(self, value: float) -> None:
        """Initially favor retaining useful state through the LSTM forget gate."""
        start, end = self.lstm.hidden_size, self.lstm.hidden_size * 2
        with torch.no_grad():
            for name, bias in self.lstm.named_parameters():
                if "bias_ih" in name:
                    bias[start:end].fill_(value)
                elif "bias_hh" in name:
                    bias[start:end].zero_()

    def forward(self, stage_ids: torch.Tensor) -> torch.Tensor:
        one_hot = torch.nn.functional.one_hot(stage_ids, num_classes=len(STAGES)).float()
        output, _ = self.lstm(one_hot)
        return self.classifier(self.dropout(output[:, -1, :]))


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)


def get_device(requested: str = "auto") -> torch.device:
    """Select the requested accelerator, preferring Apple Silicon MPS in auto mode."""
    mps_backend = getattr(torch.backends, "mps", None)
    mps_available = mps_backend is not None and mps_backend.is_available()
    cuda_available = torch.cuda.is_available()

    if requested == "auto":
        if mps_available:
            return torch.device("mps")
        if cuda_available:
            return torch.device("cuda")
        return torch.device("cpu")
    if requested == "mps":
        if not mps_available:
            raise RuntimeError("MPS is unavailable. Use --device auto or cpu instead.")
        return torch.device("mps")
    if requested == "cuda":
        if not cuda_available:
            raise RuntimeError("CUDA is unavailable. Use --device auto or cpu instead.")
        return torch.device("cuda")
    return torch.device("cpu")


def read_hypnogram(path: Path, wake_buffer_epochs: int = 60) -> list[int | None]:
    reader = pyedflib.EdfReader(str(path))
    try:
        _, durations, descriptions = reader.readAnnotations()
    finally:
        reader.close()

    epochs: list[int | None] = []
    for duration, description in zip(durations, descriptions):
        count = max(1, int(round(float(duration) / 30.0)))
        stage_name = ANNOTATION_MAP.get(str(description))
        stage_id = STAGE_TO_ID[stage_name] if stage_name is not None else None
        epochs.extend([stage_id] * count)

    sleep_indices = [i for i, stage in enumerate(epochs) if stage not in (None, STAGE_TO_ID["W"])]
    if not sleep_indices:
        return []
    start = max(0, sleep_indices[0] - wake_buffer_epochs)
    end = min(len(epochs), sleep_indices[-1] + wake_buffer_epochs + 1)
    return epochs[start:end]


def create_windows(epochs: list[int | None], sequence_length: int) -> tuple[np.ndarray, np.ndarray]:
    x: list[list[int]] = []
    y: list[int] = []
    for target_index in range(sequence_length, len(epochs)):
        sequence = epochs[target_index - sequence_length : target_index]
        target = epochs[target_index]
        if target is None or any(stage is None for stage in sequence):
            continue
        x.append([int(stage) for stage in sequence])
        y.append(int(target))
    return np.asarray(x, dtype=np.int64), np.asarray(y, dtype=np.int64)


def load_subject_data(data_dir: Path, sequence_length: int) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    subject_data: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for path in sorted(data_dir.glob("*-Hypnogram.edf")):
        subject_id = path.name[:5]
        epochs = read_hypnogram(path)
        x, y = create_windows(epochs, sequence_length)
        if len(y):
            subject_data[subject_id] = (x, y)
    if len(subject_data) < 10:
        raise RuntimeError(f"Need at least 10 subjects, found {len(subject_data)} in {data_dir}")
    return subject_data


def split_subjects(subjects: list[str], seed: int) -> tuple[list[str], list[str], list[str]]:
    shuffled = subjects.copy()
    random.Random(seed).shuffle(shuffled)
    n_subjects = len(shuffled)
    n_test = max(1, round(n_subjects * 0.15))
    n_val = max(1, round(n_subjects * 0.15))
    test = shuffled[:n_test]
    val = shuffled[n_test : n_test + n_val]
    train = shuffled[n_test + n_val :]
    return train, val, test


def combine_subjects(
    subject_data: dict[str, tuple[np.ndarray, np.ndarray]], subjects: list[str]
) -> SplitData:
    x_parts, y_parts, subject_parts = [], [], []
    for subject in subjects:
        x, y = subject_data[subject]
        x_parts.append(x)
        y_parts.append(y)
        subject_parts.append(np.repeat(subject, len(y)))
    return SplitData(
        x=np.concatenate(x_parts),
        y=np.concatenate(y_parts),
        subjects=np.concatenate(subject_parts),
    )


def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    matrix = np.zeros((len(STAGES), len(STAGES)), dtype=np.int64)
    for truth, prediction in zip(y_true, y_pred):
        matrix[int(truth), int(prediction)] += 1
    return matrix


def metrics_from_predictions(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, object]:
    matrix = confusion_matrix(y_true, y_pred)
    precision, recall, f1 = [], [], []
    for class_id in range(len(STAGES)):
        tp = matrix[class_id, class_id]
        fp = matrix[:, class_id].sum() - tp
        fn = matrix[class_id, :].sum() - tp
        p = float(tp / (tp + fp)) if tp + fp else 0.0
        r = float(tp / (tp + fn)) if tp + fn else 0.0
        score = float(2 * p * r / (p + r)) if p + r else 0.0
        precision.append(p)
        recall.append(r)
        f1.append(score)
    return {
        "accuracy": float(np.mean(y_true == y_pred)),
        "macro_precision": float(np.mean(precision)),
        "macro_recall": float(np.mean(recall)),
        "macro_f1": float(np.mean(f1)),
        "per_class_precision": dict(zip(STAGES, precision)),
        "per_class_recall": dict(zip(STAGES, recall)),
        "per_class_f1": dict(zip(STAGES, f1)),
        "confusion_matrix": matrix.tolist(),
        "n_samples": int(len(y_true)),
    }


@torch.no_grad()
def predict(model: nn.Module, loader: DataLoader, device: torch.device) -> tuple[np.ndarray, np.ndarray]:
    model.eval()
    truths, predictions = [], []
    for x, y in loader:
        logits = model(x.to(device))
        truths.append(y.numpy())
        predictions.append(logits.argmax(dim=1).cpu().numpy())
    return np.concatenate(truths), np.concatenate(predictions)


def evaluate_loss(model: nn.Module, loader: DataLoader, loss_fn: nn.Module, device: torch.device) -> float:
    model.eval()
    total_loss, total_items = 0.0, 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            loss = loss_fn(model(x), y)
            total_loss += float(loss.item()) * len(y)
            total_items += len(y)
    return total_loss / total_items


def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    loss_fn: nn.Module,
    device: torch.device,
    learning_rate: float,
    max_epochs: int,
    patience: int,
) -> tuple[nn.Module, list[dict[str, float]]]:
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    best_state = copy.deepcopy(model.state_dict())
    best_val_loss = math.inf
    epochs_without_improvement = 0
    history: list[dict[str, float]] = []

    for epoch in range(1, max_epochs + 1):
        model.train()
        total_loss, total_items, total_gradient_norm = 0.0, 0, 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            loss = loss_fn(model(x), y)
            loss.backward()
            gradient_norm = nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            total_loss += float(loss.item()) * len(y)
            total_items += len(y)
            total_gradient_norm += float(gradient_norm)

        train_loss = total_loss / total_items
        mean_gradient_norm = total_gradient_norm / len(train_loader)
        val_loss = evaluate_loss(model, val_loader, loss_fn, device)
        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "gradient_norm": mean_gradient_norm,
            }
        )
        print(
            f"epoch={epoch:02d} train_loss={train_loss:.4f} "
            f"val_loss={val_loss:.4f} grad_norm={mean_gradient_norm:.4f}"
        )

        if val_loss < best_val_loss - 1e-4:
            best_val_loss = val_loss
            best_state = copy.deepcopy(model.state_dict())
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= patience:
                print(f"Early stopping at epoch {epoch}")
                break

    model.load_state_dict(best_state)
    return model, history


def save_history(history: list[dict[str, float]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["epoch", "train_loss", "val_loss"])
        writer.writeheader()
        writer.writerows(history)


def save_confusion_csv(matrix: list[list[int]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["actual/predicted", *STAGES])
        for stage, row in zip(STAGES, matrix):
            writer.writerow([stage, *row])


def draw_training_curve(history: list[dict[str, float]], path: Path) -> None:
    width, height, margin = 900, 520, 70
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((margin, 20), "Training and validation loss", fill="black", font=font)
    draw.line((margin, height - margin, width - 30, height - margin), fill="black", width=2)
    draw.line((margin, 45, margin, height - margin), fill="black", width=2)
    values = [row[key] for row in history for key in ("train_loss", "val_loss")]
    minimum, maximum = min(values), max(values)
    scale = maximum - minimum or 1.0

    def points(key: str) -> list[tuple[float, float]]:
        result = []
        for index, row in enumerate(history):
            x = margin + index * (width - margin - 40) / max(1, len(history) - 1)
            y = height - margin - (row[key] - minimum) / scale * (height - 2 * margin)
            result.append((x, y))
        return result

    if len(history) > 1:
        draw.line(points("train_loss"), fill="#2563eb", width=3)
        draw.line(points("val_loss"), fill="#dc2626", width=3)
    draw.text((width - 220, 25), "blue: train   red: validation", fill="black", font=font)
    draw.text((10, 45), f"{maximum:.2f}", fill="black", font=font)
    draw.text((10, height - margin - 5), f"{minimum:.2f}", fill="black", font=font)
    image.save(path)


def draw_confusion_matrix(matrix: np.ndarray, path: Path) -> None:
    cell, left, top = 100, 120, 80
    width, height = left + cell * len(STAGES) + 40, top + cell * len(STAGES) + 80
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    normalized = matrix / np.maximum(matrix.sum(axis=1, keepdims=True), 1)
    draw.text((left, 20), "Confusion matrix (row-normalized color)", fill="black", font=font)
    for index, stage in enumerate(STAGES):
        draw.text((left + index * cell + 35, top - 25), stage, fill="black", font=font)
        draw.text((25, top + index * cell + 40), stage, fill="black", font=font)
    for row in range(len(STAGES)):
        for col in range(len(STAGES)):
            value = float(normalized[row, col])
            color = (int(240 - 170 * value), int(248 - 110 * value), int(255 - 25 * value))
            x0, y0 = left + col * cell, top + row * cell
            draw.rectangle((x0, y0, x0 + cell, y0 + cell), fill=color, outline="white")
            text = f"{matrix[row, col]}\n{value:.1%}"
            draw.multiline_text((x0 + 30, y0 + 34), text, fill="black", font=font, align="center")
    draw.text((left + 160, height - 30), "Predicted stage", fill="black", font=font)
    draw.text((5, top - 45), "Actual", fill="black", font=font)
    image.save(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--sequence-length", type=int, default=20)
    parser.add_argument("--hidden-size", type=int, default=32)
    parser.add_argument("--num-layers", type=int, default=1)
    parser.add_argument("--dropout", type=float, default=0.2)
    parser.add_argument(
        "--forget-gate-bias",
        type=float,
        default=1.0,
        help="Initial bias for the LSTM forget gate",
    )
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument(
        "--transition-weight",
        type=float,
        default=4.0,
        help="Sampling weight for sequences whose target differs from the last input stage",
    )
    parser.add_argument("--max-epochs", type=int, default=50)
    parser.add_argument("--patience", type=int, default=7)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument(
        "--device",
        choices=("auto", "mps", "cuda", "cpu"),
        default="auto",
        help="Training device; auto prefers MPS, then CUDA, then CPU",
    )
    args = parser.parse_args()

    set_seed(args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    subject_data = load_subject_data(args.data_dir, args.sequence_length)
    train_subjects, val_subjects, test_subjects = split_subjects(list(subject_data), args.seed)
    train_data = combine_subjects(subject_data, train_subjects)
    val_data = combine_subjects(subject_data, val_subjects)
    test_data = combine_subjects(subject_data, test_subjects)

    generator = torch.Generator().manual_seed(args.seed)
    if args.transition_weight > 1.0:
        sample_weights = np.ones(len(train_data.y), dtype=np.float64)
        sample_weights[train_data.y != train_data.x[:, -1]] = args.transition_weight
        sampler = WeightedRandomSampler(
            weights=torch.as_tensor(sample_weights, dtype=torch.double),
            num_samples=len(sample_weights),
            replacement=True,
            generator=generator,
        )
        train_loader = DataLoader(
            SequenceDataset(train_data), batch_size=args.batch_size, sampler=sampler
        )
    else:
        train_loader = DataLoader(
            SequenceDataset(train_data),
            batch_size=args.batch_size,
            shuffle=True,
            generator=generator,
        )
    val_loader = DataLoader(SequenceDataset(val_data), batch_size=args.batch_size)
    test_loader = DataLoader(SequenceDataset(test_data), batch_size=args.batch_size)

    counts = np.bincount(train_data.y, minlength=len(STAGES))
    class_weights = np.sqrt(len(train_data.y) / (len(STAGES) * np.maximum(counts, 1)))
    device = get_device(args.device)
    print(f"Using device: {device}")
    loss_fn = nn.CrossEntropyLoss(weight=torch.tensor(class_weights, dtype=torch.float32, device=device))
    model = SleepStageLSTM(
        args.hidden_size,
        args.num_layers,
        args.dropout,
        forget_gate_bias=args.forget_gate_bias,
    ).to(device)
    model, history = train_model(
        model,
        train_loader,
        val_loader,
        loss_fn,
        device,
        args.learning_rate,
        args.max_epochs,
        args.patience,
    )

    y_true, y_pred = predict(model, test_loader, device)
    lstm_metrics = metrics_from_predictions(y_true, y_pred)
    baseline_pred = test_data.x[:, -1]
    baseline_metrics = metrics_from_predictions(test_data.y, baseline_pred)

    transition_mask = test_data.y != test_data.x[:, -1]
    transition_lstm = metrics_from_predictions(test_data.y[transition_mask], y_pred[transition_mask])
    transition_baseline = metrics_from_predictions(
        test_data.y[transition_mask], baseline_pred[transition_mask]
    )

    results = {
        "configuration": {
            "sequence_length": args.sequence_length,
            "input_size": len(STAGES),
            "hidden_size": args.hidden_size,
            "num_layers": args.num_layers,
            "dropout": args.dropout,
            "forget_gate_bias": args.forget_gate_bias,
            "batch_size": args.batch_size,
            "learning_rate": args.learning_rate,
            "transition_weight": args.transition_weight,
            "max_epochs": args.max_epochs,
            "patience": args.patience,
            "seed": args.seed,
            "device": str(device),
        },
        "data": {
            "n_subjects": len(subject_data),
            "train_subjects": train_subjects,
            "validation_subjects": val_subjects,
            "test_subjects": test_subjects,
            "train_sequences": len(train_data.y),
            "validation_sequences": len(val_data.y),
            "test_sequences": len(test_data.y),
            "train_target_counts": dict(zip(STAGES, counts.tolist())),
            "transition_test_sequences": int(transition_mask.sum()),
        },
        "lstm_all_epochs": lstm_metrics,
        "last_stage_baseline_all_epochs": baseline_metrics,
        "lstm_transition_epochs": transition_lstm,
        "last_stage_baseline_transition_epochs": transition_baseline,
        "best_epoch": min(history, key=lambda row: row["val_loss"])["epoch"],
    }

    (args.output_dir / "metrics.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    save_history(history, args.output_dir / "training_history.csv")
    save_confusion_csv(lstm_metrics["confusion_matrix"], args.output_dir / "confusion_matrix.csv")
    draw_training_curve(history, args.output_dir / "training_curve.png")
    draw_confusion_matrix(np.asarray(lstm_metrics["confusion_matrix"]), args.output_dir / "confusion_matrix.png")
    torch.save(model.state_dict(), args.output_dir / "model.pt")

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

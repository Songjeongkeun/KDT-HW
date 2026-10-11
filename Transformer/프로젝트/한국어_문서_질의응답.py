"""KLUE-RoBERTa를 KorQuAD 1.0으로 학습·평가하고 새 문장의 답을 예측한다.

사용법은 ``python 한국어_문서_질의응답_KorQuAD.py --help``를 참조한다.
``--smoke``는 소규모 실행 점검이며 최종 성능 평가가 아니다.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import load_dataset
from sklearn.model_selection import GroupShuffleSplit
from transformers import (
    AutoModelForQuestionAnswering,
    AutoTokenizer,
    DefaultDataCollator,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "klue/roberta-base"
DATASET_NAME = "KorQuAD/squad_kor_v1"
SEED = 2026
MAX_LENGTH = 384
DOC_STRIDE = 128
N_BEST_SIZE = 20
MAX_ANSWER_LENGTH = 40
DEFAULT_CONTEXT = (
    "도서관은 평일 오전 9시부터 오후 8시까지 운영한다. "
    "토요일에는 오전 10시부터 오후 5시까지 운영하며, 일요일과 공휴일에는 휴관한다."
)
DEFAULT_QUESTION = "토요일 도서관 운영 시간은 언제인가요?"


def set_seed_and_device() -> torch.device:
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return torch.device("xpu")
    return torch.device("cpu")


def load_splits(smoke: bool):
    dataset = load_dataset(DATASET_NAME)
    all_train = dataset["train"]
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.1, random_state=SEED)
    train_indices, selection_indices = next(
        splitter.split(np.zeros(len(all_train)), groups=all_train["title"])
    )
    train_examples = all_train.select(train_indices)
    selection_examples = all_train.select(selection_indices)
    final_examples = dataset["validation"]
    assert set(train_examples["title"]).isdisjoint(selection_examples["title"])
    if smoke:
        train_examples = train_examples.shuffle(seed=SEED).select(
            range(min(256, len(train_examples)))
        )
        selection_examples = selection_examples.shuffle(seed=SEED).select(
            range(min(64, len(selection_examples)))
        )
        final_examples = final_examples.shuffle(seed=SEED).select(
            range(min(64, len(final_examples)))
        )
    return train_examples, selection_examples, final_examples


def load_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    if not tokenizer.is_fast:
        raise RuntimeError("정답 위치 변환에는 Fast tokenizer가 필요합니다.")
    return tokenizer


def tokenize_pairs(tokenizer, questions, contexts, *, return_tensors=None):
    options = {
        "truncation": "only_second",
        "max_length": MAX_LENGTH,
        "stride": DOC_STRIDE,
        "return_overflowing_tokens": True,
        "return_offsets_mapping": True,
        # KLUE-RoBERTa의 type_vocab_size는 1이므로 구분 ID를 전달하지 않는다.
        "return_token_type_ids": False,
        "padding": "max_length",
    }
    if return_tensors is not None:
        options["return_tensors"] = return_tensors
    return tokenizer(questions, contexts, **options)


def tokenize_train(examples, tokenizer):
    encoded = tokenize_pairs(
        tokenizer,
        [question.strip() for question in examples["question"]],
        examples["context"],
    )
    sample_map = encoded.pop("overflow_to_sample_mapping")
    offset_maps = encoded.pop("offset_mapping")
    start_positions, end_positions = [], []

    for feature_index, offsets in enumerate(offset_maps):
        answer = examples["answers"][sample_map[feature_index]]
        answer_start = answer["answer_start"][0]
        answer_end = answer_start + len(answer["text"][0])
        sequence_ids = encoded.sequence_ids(feature_index)
        cls_index = encoded["input_ids"][feature_index].index(tokenizer.cls_token_id)
        context_tokens = [i for i, sid in enumerate(sequence_ids) if sid == 1]

        if not context_tokens:
            start_positions.append(cls_index)
            end_positions.append(cls_index)
            continue

        context_start, context_end = context_tokens[0], context_tokens[-1]
        if offsets[context_start][0] > answer_start or offsets[context_end][1] < answer_end:
            start_positions.append(cls_index)
            end_positions.append(cls_index)
            continue

        token_start = context_start
        while token_start <= context_end and offsets[token_start][0] <= answer_start:
            token_start += 1
        token_end = context_end
        while token_end >= context_start and offsets[token_end][1] >= answer_end:
            token_end -= 1
        start_positions.append(token_start - 1)
        end_positions.append(token_end + 1)

    encoded["start_positions"] = start_positions
    encoded["end_positions"] = end_positions
    return encoded


def tokenize_eval(examples, tokenizer):
    encoded = tokenize_pairs(
        tokenizer,
        [question.strip() for question in examples["question"]],
        examples["context"],
    )
    sample_map = encoded.pop("overflow_to_sample_mapping")
    encoded["example_id"] = []
    for feature_index, sample_index in enumerate(sample_map):
        encoded["example_id"].append(examples["id"][sample_index])
        sequence_ids = encoded.sequence_ids(feature_index)
        encoded["offset_mapping"][feature_index] = [
            offset if sequence_ids[i] == 1 else None
            for i, offset in enumerate(encoded["offset_mapping"][feature_index])
        ]
    return encoded


def make_train_features(examples, tokenizer):
    features = examples.map(
        tokenize_train,
        batched=True,
        remove_columns=examples.column_names,
        fn_kwargs={"tokenizer": tokenizer},
    )
    if "token_type_ids" in features.column_names:
        raise RuntimeError("KLUE-RoBERTa 입력에 token_type_ids가 남아 있습니다.")
    for row in features:
        start, end = row["start_positions"], row["end_positions"]
        if not (0 <= start <= end < len(row["input_ids"])):
            raise ValueError("정답 토큰 위치가 입력 길이를 벗어났습니다.")
    return features


def make_eval_features(examples, tokenizer):
    return examples.map(
        tokenize_eval,
        batched=True,
        remove_columns=examples.column_names,
        fn_kwargs={"tokenizer": tokenizer},
    )


def postprocess_qa(examples, features, start_logits, end_logits):
    features_by_id = defaultdict(list)
    for feature_index, feature in enumerate(features):
        features_by_id[feature["example_id"]].append(feature_index)

    predictions = {}
    for example in examples:
        context = example["context"]
        best_answer, best_score, best_span = "", -float("inf"), None
        for feature_index in features_by_id[example["id"]]:
            offsets = features[feature_index]["offset_mapping"]
            starts = np.argsort(start_logits[feature_index])[-N_BEST_SIZE:][::-1]
            ends = np.argsort(end_logits[feature_index])[-N_BEST_SIZE:][::-1]
            for start_index in starts:
                for end_index in ends:
                    if offsets[start_index] is None or offsets[end_index] is None:
                        continue
                    if end_index < start_index or end_index - start_index + 1 > MAX_ANSWER_LENGTH:
                        continue
                    char_start = offsets[start_index][0]
                    char_end = offsets[end_index][1]
                    if not (0 <= char_start < char_end <= len(context)):
                        continue
                    score = float(
                        start_logits[feature_index][start_index]
                        + end_logits[feature_index][end_index]
                    )
                    if score > best_score:
                        best_answer = context[char_start:char_end]
                        best_score = score
                        best_span = (char_start, char_end)
        predictions[example["id"]] = {
            "answer": best_answer,
            "span": best_span,
            "score": best_score,
        }
    return predictions


def normalize_answer(text: str) -> str:
    text = str(text).lower()
    text = "".join(char for char in text if not unicodedata.category(char).startswith("P"))
    return re.sub(r"\s+", "", text)


def char_f1(prediction: str, truth: str) -> float:
    predicted_chars = list(normalize_answer(prediction))
    gold_chars = list(normalize_answer(truth))
    if not predicted_chars or not gold_chars:
        return float(predicted_chars == gold_chars)
    overlap = sum((Counter(predicted_chars) & Counter(gold_chars)).values())
    if overlap == 0:
        return 0.0
    precision = overlap / len(predicted_chars)
    recall = overlap / len(gold_chars)
    return 2 * precision * recall / (precision + recall)


def score_one(prediction: str, gold_answers: list[str]):
    return (
        max(float(normalize_answer(prediction) == normalize_answer(gold)) for gold in gold_answers),
        max(char_f1(prediction, gold) for gold in gold_answers),
    )


def summarize_predictions(examples, predictions, smoke: bool):
    rows = []
    for example in examples:
        predicted = predictions[example["id"]]["answer"]
        golds = example["answers"]["text"]
        em, f1 = score_one(predicted, golds)
        rows.append({
            "id": example["id"],
            "title": example["title"],
            "question": example["question"],
            "prediction": predicted,
            "gold": golds[0],
            "em": em,
            "char_f1": f1,
            "context_length": len(example["context"]),
        })
    result = pd.DataFrame(rows)
    metrics = {
        "normalized_em": float(result["em"].mean() * 100),
        "character_f1": float(result["char_f1"].mean() * 100),
        "examples": len(result),
        "smoke_test": smoke,
        "official_korquad_score": False,
    }
    bins = pd.cut(
        result["context_length"],
        bins=[0, 500, 1000, 2000, float("inf")],
        labels=["500자 이하", "501~1000자", "1001~2000자", "2000자 초과"],
    )
    by_length = result.groupby(bins, observed=True).agg(
        count=("id", "count"),
        em=("em", "mean"),
        char_f1=("char_f1", "mean"),
    )
    return result, metrics, by_length


def evaluate_model(model, tokenizer, examples, output_dir: Path, smoke: bool, device):
    features = make_eval_features(examples, tokenizer)
    inputs = features.remove_columns(["example_id", "offset_mapping"])
    args = TrainingArguments(
        output_dir=str(output_dir / "eval_tmp"),
        per_device_eval_batch_size=8,
        report_to="none",
        fp16=(device.type == "cuda"),
    )
    evaluator = Trainer(
        model=model,
        args=args,
        data_collator=DefaultDataCollator(),
    )
    output = evaluator.predict(inputs)
    start_logits, end_logits = output.predictions[:2]
    predictions = postprocess_qa(examples, features, start_logits, end_logits)
    result, metrics, by_length = summarize_predictions(examples, predictions, smoke)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    result.to_csv(output_dir / "predictions.csv", index=False, encoding="utf-8-sig")
    by_length.to_csv(output_dir / "length_analysis.csv", encoding="utf-8-sig")
    result.loc[result["em"] == 0].sort_values("char_f1").head(20).to_csv(
        output_dir / "error_examples.csv", index=False, encoding="utf-8-sig"
    )
    print("공개 검증 결과:", json.dumps(metrics, ensure_ascii=False))
    print("문단 길이별 분석:\n", by_length)
    print("오류 사례:\n", result.loc[result["em"] == 0, ["question", "gold", "prediction"]].head(5))
    return metrics


def answer_question(question: str, context: str, model, tokenizer):
    if not question.strip() or not context.strip():
        raise ValueError("질문과 문단을 모두 입력하세요.")
    encoded = tokenize_pairs(
        tokenizer,
        question.strip(),
        context,
        return_tensors="pt",
    )
    sequence_ids = [encoded.sequence_ids(i) for i in range(encoded["input_ids"].shape[0])]
    offsets = encoded.pop("offset_mapping").tolist()
    encoded.pop("overflow_to_sample_mapping", None)
    device = next(model.parameters()).device
    inputs = {key: value.to(device) for key, value in encoded.items()}
    model.eval()
    with torch.no_grad():
        output = model(**inputs)
    features = []
    for window_index, window_offsets in enumerate(offsets):
        features.append({
            "example_id": "user_input",
            "offset_mapping": [
                offset if sequence_ids[window_index][token_index] == 1 else None
                for token_index, offset in enumerate(window_offsets)
            ],
        })
    example = [{"id": "user_input", "context": context}]
    return postprocess_qa(
        example,
        features,
        output.start_logits.cpu().numpy(),
        output.end_logits.cpu().numpy(),
    )["user_input"]


def run_train(args, device):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir or f"outputs/korquad_qa_script/{'smoke' if args.smoke else 'full'}_{stamp}")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"출력 폴더에 이미 파일이 있습니다: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    train_examples, selection_examples, final_examples = load_splits(args.smoke)
    tokenizer = load_tokenizer()
    train_features = make_train_features(train_examples, tokenizer)
    selection_features = make_train_features(selection_examples, tokenizer)
    print("데이터:", len(train_examples), len(selection_examples), len(final_examples))
    print("토큰 창:", len(train_features), len(selection_features))

    model = AutoModelForQuestionAnswering.from_pretrained(MODEL_NAME)
    training_args = TrainingArguments(
        output_dir=str(output_dir / "checkpoints"),
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        gradient_accumulation_steps=2,
        num_train_epochs=1 if args.smoke else args.epochs,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        save_total_limit=2,
        logging_strategy="epoch",
        report_to="none",
        seed=SEED,
        fp16=(device.type == "cuda"),
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_features,
        eval_dataset=selection_features,
        processing_class=tokenizer,
        data_collator=DefaultDataCollator(),
    )
    train_result = trainer.train()
    model_dir = output_dir / "model"
    trainer.save_model(str(model_dir))
    tokenizer.save_pretrained(str(model_dir))
    pd.DataFrame(trainer.state.log_history).to_csv(
        output_dir / "training_history.csv", index=False, encoding="utf-8-sig"
    )
    summary = {
        "model": MODEL_NAME,
        "dataset": DATASET_NAME,
        "seed": SEED,
        "device": str(device),
        "smoke_test": args.smoke,
        "train_examples": len(train_examples),
        "selection_examples": len(selection_examples),
        "public_validation_examples": len(final_examples),
        "train_features": len(train_features),
        "selection_features": len(selection_features),
        "num_train_epochs": args.epochs if not args.smoke else 1,
        "training_metrics": train_result.metrics,
        "best_checkpoint": trainer.state.best_model_checkpoint,
        "best_eval_loss": trainer.state.best_metric,
    }
    (output_dir / "run_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("학습 기록:", json.dumps(summary, ensure_ascii=False, indent=2))
    evaluate_model(trainer.model, tokenizer, final_examples, output_dir, args.smoke, device)
    prediction = answer_question(DEFAULT_QUESTION, DEFAULT_CONTEXT, trainer.model, tokenizer)
    sample = {"question": DEFAULT_QUESTION, "context": DEFAULT_CONTEXT, **prediction}
    (output_dir / "new_example_prediction.json").write_text(
        json.dumps(sample, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("새 문장 예측:", json.dumps(sample, ensure_ascii=False))
    print("결과 폴더:", output_dir.resolve())


def run_evaluate(args, device):
    if not Path(args.checkpoint).exists():
        raise FileNotFoundError(f"모델 경로를 찾을 수 없습니다: {args.checkpoint}")
    tokenizer = load_tokenizer()
    model = AutoModelForQuestionAnswering.from_pretrained(args.checkpoint)
    _, _, final_examples = load_splits(args.smoke)
    output_dir = Path(args.output_dir or f"outputs/korquad_qa_script/evaluation_{datetime.now():%Y%m%d_%H%M%S}")
    evaluate_model(model, tokenizer, final_examples, output_dir, args.smoke, device)
    print("결과 폴더:", output_dir.resolve())


def run_predict(args, device):
    if not Path(args.checkpoint).exists():
        raise FileNotFoundError(f"모델 경로를 찾을 수 없습니다: {args.checkpoint}")
    tokenizer = load_tokenizer()
    model = AutoModelForQuestionAnswering.from_pretrained(args.checkpoint).to(device)
    question = args.question or DEFAULT_QUESTION
    context = args.context or DEFAULT_CONTEXT
    prediction = answer_question(question, context, model, tokenizer)
    print(json.dumps({"question": question, "context": context, **prediction}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="mode", required=True)
    train_parser = commands.add_parser("train", help="사전학습 모델 파인튜닝과 평가")
    train_parser.add_argument("--smoke", action="store_true", help="소규모 실행 점검; 제출용 성능 아님")
    train_parser.add_argument("--epochs", type=int, default=3, choices=range(1, 21), metavar="1-20", help="전체 학습 epoch 수 (기본: 3, --smoke에서는 1로 고정)")
    train_parser.add_argument("--output-dir", help="새 결과 폴더 (기본: 시간별 자동 생성)")
    eval_parser = commands.add_parser("evaluate", help="저장한 모델의 공개 검증 평가")
    eval_parser.add_argument("--checkpoint", required=True, help="파인튜닝 모델 또는 체크포인트 폴더")
    eval_parser.add_argument("--smoke", action="store_true", help="공개 검증 64개만 평가")
    eval_parser.add_argument("--output-dir", help="평가 파일 저장 폴더")
    predict_parser = commands.add_parser("predict", help="새 질문·문단 예측")
    predict_parser.add_argument("--checkpoint", required=True, help="파인튜닝 모델 또는 체크포인트 폴더")
    predict_parser.add_argument("--question", help="입력 질문")
    predict_parser.add_argument("--context", help="입력 문단")
    args = parser.parse_args()
    device = set_seed_and_device()
    print("장치:", device)
    if args.mode == "train":
        run_train(args, device)
    elif args.mode == "evaluate":
        run_evaluate(args, device)
    else:
        run_predict(args, device)


if __name__ == "__main__":
    main()

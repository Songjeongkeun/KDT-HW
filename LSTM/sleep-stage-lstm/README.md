# LSTM 기반 다음 수면 단계 예측

직전 10분의 수면 단계 시퀀스로 다음 30초의 수면 단계
`W / N1 / N2 / N3 / REM`을 예측하는 미니 프로젝트입니다.

## 핵심 결과

사람 단위로 분리한 테스트 세트 6,293개 시퀀스에서 얻은 결과입니다.

| 모델 | 전체 Accuracy | 전체 Macro F1 | 전환 구간 Accuracy | 전환 구간 Macro F1 |
|---|---:|---:|---:|---:|
| 마지막 단계 기준모델 | 91.98% | 85.51% | 0.00% | 0.00% |
| 표준 LSTM | **92.02%** | **85.95%** | 12.48% | 9.16% |
| 전환 가중 LSTM | 89.19% | 81.67% | **37.62%** | **31.89%** |

전체 정확도만 보면 표준 LSTM과 기준모델의 차이는 거의 없습니다. 이는 테스트
시퀀스 중 약 92%에서 다음 단계가 직전 단계와 같기 때문입니다. 전환 시퀀스를
4배 자주 학습한 모델은 전체 정확도는 낮아졌지만, 실제 단계가 바뀌는 구간의
정확도가 12.48%에서 37.62%로 증가했습니다.

![전환 가중 LSTM 혼동행렬](results_weighted/confusion_matrix.png)

## 데이터

- 출처: [PhysioNet Sleep-EDF Expanded](https://physionet.org/content/sleep-edfx/1.0.0/)
- 사용 자료: `sleep-cassette`의 사람별 첫 번째 Hypnogram 40개
- 시간 단위: 30초 epoch
- 클래스: W, N1, N2, N3, REM
- 전처리: 기존 stage 3과 4를 N3로 통합하고 Movement/Unknown 제거
- 긴 각성 구간의 영향을 줄이기 위해 첫 수면 전·마지막 수면 후 30분만 유지
- 라이선스: Open Data Commons Attribution License v1.0

원본 Hypnogram은 저장소에 포함하지 않습니다.

## LSTM 입력

각 수면 단계를 5차원 one-hot vector로 변환합니다.

```text
(batch_size, sequence_length, input_size)
(B, 20, 5)
```

- `B`: 한 번에 처리하는 시퀀스 개수
- `20`: 직전 20개 × 30초 = 10분
- `5`: W, N1, N2, N3, REM one-hot feature

## 모델

```text
20개 수면 단계 one-hot sequence
        ↓
1-layer LSTM (hidden_size=32)
        ↓
Dropout(0.2)
        ↓
Linear(32 → 5)
        ↓
다음 30초 수면 단계
```

기본 실행은 전환 시퀀스를 4배의 확률로 표본 추출합니다. Loss에는 완만한
제곱근 역빈도 클래스 가중치를 적용합니다.

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/download_data.py --output-dir data/raw --max-subjects 40
python src/train.py --data-dir data/raw --output-dir results_weighted
```

Apple Silicon Mac에서는 MPS가 자동으로 선택됩니다. 특정 장치를 지정하려면
`--device mps`를 사용하며, `--device cpu`로 CPU 실행을 강제할 수 있습니다.
Forget gate bias는 기본값 `1.0`이며, `--forget-gate-bias`로 변경할 수 있습니다.

표준 LSTM은 전환 가중치를 1로 설정합니다.

```bash
python src/train.py \
  --data-dir data/raw \
  --output-dir results \
  --transition-weight 1
```

## 생성 결과

- `metrics.json`: 설정, 사람 분할, 전체 지표와 전환 구간 지표
- `training_history.csv`: epoch별 학습·검증 loss
- `confusion_matrix.csv`: 실제/예측 클래스별 개수
- `confusion_matrix.png`: 행 정규화 혼동행렬
- `training_curve.png`: 학습 곡선
- `model.pt`: 학습된 PyTorch 가중치

## 데이터 누수 방지

겹치는 sliding window를 무작위로 나누면 거의 동일한 시퀀스가 학습과 테스트에
동시에 포함될 수 있습니다. 이 프로젝트는 40명을 다음처럼 먼저 분리한 뒤 각
사람 내부에서 시퀀스를 생성합니다.

- 학습: 28명
- 검증: 6명
- 테스트: 6명

따라서 테스트 결과는 학습에서 보지 못한 사람의 수면 기록에 대한 결과입니다.

## 프로젝트 구조

```text
sleep-stage-lstm/
├── README.md
├── requirements.txt
├── sleep_stage_lstm.ipynb
├── data/
│   └── README.md
├── src/
│   ├── download_data.py
│   └── train.py
├── results/
├── results_weighted/
└── report/
    └── project_report.md
```

## 재현성

기본 random seed는 2026이며, PyTorch deterministic algorithm을 사용합니다. 실행
환경이나 PyTorch 버전에 따라 부동소수점 수준의 차이가 생길 수 있습니다.

LSTM의 forget gate bias는 1로 초기화해 초기에 기존 상태를 보존하도록 유도합니다.
학습 로그의 `grad_norm`은 gradient clipping 전 평균 L2 norm이며, 긴 시퀀스에서
그래디언트 소실·폭주를 점검하는 데 사용합니다.

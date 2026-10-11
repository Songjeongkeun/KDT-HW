# 이안류 CCTV 객체 탐지

제공된 CCTV 이미지와 JSON Annotation을 YOLO Detect 형식으로 변환하고, YOLO11n 학습·평가·추론을 수행하는 과제다.

## 구성

```text
이안류 CCTV 데이터/
├── README.md
├── requirements.txt
├── start_jupyter.ps1
├── 이안류_CCTV_YOLO_Detect_학습과_추론.ipynb
├── inputs/README.md
├── yolo_ripcurrent_detect/data.yaml
└── report/
    ├── 학습결과.md
    ├── training_history.csv
    └── figures/
```

원본 데이터, 가상환경, 이미지·라벨 변환 산출물, 모델 가중치와 실행 로그는 Git에서 제외한다. 노트북의 긴 출력과 내장 이미지는 제거하고 실험 결과는 `report/`에 따로 정리했다.

## 실행 환경

기록된 실험 환경은 Windows, Python 3.12, PyTorch 2.7.1+cu118, torchvision 0.22.1+cu118, Ultralytics 8.4.163이다. 다음 명령은 이 폴더에서 PowerShell로 실행한다.

```powershell
py -3.12 -m venv .venv
# NVIDIA GPU 환경: 먼저 CUDA 11.8용 PyTorch를 설치한다.
.\.venv\Scripts\python.exe -m pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cu118
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m ipykernel install --sys-prefix --name riptide-cctv --display-name "Python (.venv) - Riptide CCTV"
```

NVIDIA GPU를 사용하지 않는 경우 CUDA 전용 설치 명령을 생략한다. GPU 확인:

```powershell
.\.venv\Scripts\python.exe -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

VS Code에서 노트북을 열고 이 폴더의 `.venv` 커널을 선택한다. 커널 포트 오류가 있으면 `./start_jupyter.ps1`을 실행하고, 출력된 토큰 포함 URL로 **커널 선택 → 다른 커널 선택 → Existing Jupyter Server**에 연결한다. 서버는 `127.0.0.1:8888`에서만 수신하며 인증을 유지한다. 접속 토큰을 Git에 저장하지 않는다.

## 데이터 준비

원본 데이터는 별도로 확보하고 이용 조건을 확인한다. 기본 경로는 다음과 같다.

```text
290.이안류 CCTV 데이터/
└── 01-1.정식개방데이터/
    ├── Training/
    │   ├── 01.원천데이터/
    │   └── 02.라벨링데이터/
    └── Validation/
        ├── 01.원천데이터/
        └── 02.라벨링데이터/
```

원본을 다른 위치에 보관했다면 Jupyter를 시작하기 전에 설정한다.

```powershell
$env:RIPCURRENT_DATA_ROOT = 'D:\데이터\290.이안류 CCTV 데이터\01-1.정식개방데이터'
```

이미지 복제를 피하기 위해 하드링크를 사용한다. 원본 데이터와 이 프로젝트의 출력 폴더는 같은 드라이브의 하드링크 지원 파일시스템에 두어야 한다. 관리자 권한이 필요한 심볼릭 링크는 사용하지 않는다.

## 노트북 실행 순서

1. 원본 데이터 경로와 이미지·JSON 개수를 확인한다.
2. `annotations.drawing`을 둘러싸는 사각형을 계산한다.
3. YOLO의 `class_id x_center y_center width height` 형식으로 좌표를 정규화한다. `class=1`, `object=Yes`는 이안류, 음성 이미지는 배경으로 사용한다.
4. 제공된 Train / Validation 분할을 유지하고 `data.yaml`을 생성한다.
5. YOLO11n을 학습한다. 기본값은 10 epoch, 이미지 크기 640, batch 4, 학습 비율 25%다. 변환과 검증은 전체 데이터를 사용한다.
6. `best.pt`를 검증하고 Loss, Precision, Recall, mAP 및 그래프를 확인한다.
7. `INFERENCE_SOURCE`에 새 이미지 또는 영상 경로를 지정해 추론한다.
8. 저장된 이미지·영상의 Bounding Box와 Confidence Score를 확인한다.

`INFERENCE_SOURCE = None`은 검증 이미지 한 장으로 기능만 확인한다. 새 CCTV 데이터에 대한 추론 완료를 의미하지 않는다. 새 입력 파일은 [inputs/](inputs/README.md)에 두면 Git에서 제외된다.

## 기록된 결과

학습 이미지 62,035장으로 10 epoch를 완료했다. `best.pt` 재평가 결과는 Precision **0.6287**, Recall **0.4779**, mAP50 **0.5457**, mAP50–95 **0.2609**다.

자세한 설정·Loss·그래프와 한계는 [학습 결과 보고서](report/학습결과.md)를 참고한다. `fraction=0.25`가 무작위 추출이 아니라 정렬된 앞부분 선택이라는 점에 주의한다.

`best.pt`는 Git에 포함하지 않는다. 새 환경에서는 먼저 학습하거나 별도로 보관한 가중치를 로컬 `runs/detect/<실행명>/weights/best.pt`에 두고, 노트북의 `RUN_DIR`과 `BEST_MODEL_PATH`를 해당 경로로 설정한 후 평가·추론 셀을 실행한다.

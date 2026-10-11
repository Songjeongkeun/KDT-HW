# 새 CCTV 입력

별도의 CCTV 이미지 또는 영상을 이 폴더에 넣고 노트북에서 다음과 같이 지정한다.

```python
INFERENCE_SOURCE = PROJECT_ROOT / 'inputs' / 'new_cctv.jpg'
# INFERENCE_SOURCE = PROJECT_ROOT / 'inputs' / 'new_cctv.mp4'
```

실제 입력 파일은 Git에서 제외한다. `INFERENCE_SOURCE = None`이면 검증 이미지 한 장으로 기능을 확인하며, 별도 새 데이터에 대한 테스트는 아니다.

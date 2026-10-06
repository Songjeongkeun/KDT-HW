# WebRTC 프로젝트 진행 가이드

## 1. 추천 프로젝트 주제

### 1:1 화상 스터디룸

사용자가 방 번호를 입력해서 입장하면 같은 방에 들어온 두 명이 화상 통화를 할 수 있는 서비스입니다.

과제 요구사항과 연결:

- RTCPeerConnection 사용
- offer / answer 처리
- ICE Candidate 처리
- 화상 채팅 구현
- 선택 기능으로 화면 공유 구현

## 2. 기술 스택

### 프론트엔드

- HTML
- CSS
- JavaScript
- WebRTC API
- Socket.IO client

### 백엔드

- Node.js
- Express
- Socket.IO

### 개발 환경

- Chrome 브라우저 권장
- 로컬 테스트: `http://localhost:3000`
- 같은 네트워크의 다른 기기 테스트 시 HTTPS 또는 로컬 네트워크 설정 필요

## 3. 폴더 구조

```text
webrtc-study-room/
├─ package.json
├─ server.js
└─ public/
   ├─ index.html
   ├─ style.css
   └─ client.js
```

## 4. 역할 분담 추천

### 백엔드 담당

- Express 서버 구성
- Socket.IO 연결 처리
- 방 입장/퇴장 이벤트 처리
- offer, answer, ice-candidate 전달

### WebRTC 담당

- RTCPeerConnection 생성
- getUserMedia 처리
- offer / answer 생성 및 적용
- ICE candidate 송수신
- 화면 공유 트랙 교체

### UI 담당

- 방 입장 화면
- 내 영상/상대 영상 영역
- 마이크/카메라/화면 공유 버튼
- 연결 상태 표시

### 발표/문서 담당

- WebRTC 동작 흐름 정리
- 구현 기능 캡처
- 어려웠던 점과 해결 방법 정리
- 발표 자료 제작

## 5. 개발 순서

### 1단계: 서버 기본 구성

목표:

- `localhost:3000` 접속 가능
- 정적 파일 제공
- Socket.IO 연결 확인

완료 기준:

- 브라우저에서 페이지가 열린다.
- 서버 콘솔에 사용자의 접속 로그가 찍힌다.

### 2단계: 방 입장 구현

목표:

- 사용자가 방 번호를 입력한다.
- 서버가 같은 방에 있는 사용자끼리만 이벤트를 전달한다.

Socket.IO 이벤트 예시:

```js
socket.emit("join-room", roomId);
socket.to(roomId).emit("user-joined", socket.id);
```

완료 기준:

- 두 브라우저가 같은 방에 들어가면 서로 입장 이벤트를 받는다.
- 다른 방 사용자에게는 이벤트가 가지 않는다.

### 3단계: 로컬 영상 표시

목표:

- `getUserMedia()`로 카메라/마이크 권한을 요청한다.
- 내 영상을 화면에 표시한다.

완료 기준:

- 내 카메라 화면이 보인다.
- 마이크/카메라 권한 거부 시 안내 메시지가 나온다.

### 4단계: PeerConnection 생성

목표:

- `RTCPeerConnection`을 만든다.
- 로컬 미디어 트랙을 추가한다.
- 상대방 트랙 수신 이벤트를 등록한다.

완료 기준:

- `connectionState`, `iceConnectionState` 로그가 찍힌다.

### 5단계: Offer / Answer 처리

목표:

- 먼저 들어와 있던 사용자가 offer를 만든다.
- 새로 들어온 사용자가 answer를 만든다.
- 두 브라우저가 remote/local description을 정상 설정한다.

완료 기준:

- 콘솔에서 offer, answer 이벤트 흐름을 확인할 수 있다.
- signaling state가 `stable` 상태로 돌아온다.

### 6단계: ICE Candidate 처리

목표:

- `onicecandidate`에서 candidate를 서버로 보낸다.
- 상대방 candidate를 받아 `addIceCandidate()`를 호출한다.

완료 기준:

- 두 브라우저 사이에 영상/음성이 연결된다.
- `connectionState`가 `connected` 또는 `completed`가 된다.

### 7단계: 통화 제어 기능

목표:

- 마이크 켜기/끄기
- 카메라 켜기/끄기
- 나가기

완료 기준:

- 버튼을 눌렀을 때 실제 트랙의 `enabled` 값이 바뀐다.

### 8단계: 화면 공유

목표:

- `getDisplayMedia()`로 화면 공유 스트림을 얻는다.
- 기존 비디오 트랙을 화면 공유 트랙으로 교체한다.

핵심 코드:

```js
const screenStream = await navigator.mediaDevices.getDisplayMedia({
  video: true
});

const screenTrack = screenStream.getVideoTracks()[0];
const sender = peerConnection
  .getSenders()
  .find((sender) => sender.track && sender.track.kind === "video");

await sender.replaceTrack(screenTrack);
```

완료 기준:

- 상대방 화면에 내 카메라 대신 공유 화면이 보인다.
- 화면 공유 종료 시 카메라로 복귀한다.

## 6. 최소 기능 체크리스트

- [ ] 방 번호 입력
- [ ] 같은 방 사용자끼리만 연결
- [ ] 내 카메라/마이크 표시
- [ ] 상대방 영상/음성 표시
- [ ] RTCPeerConnection 사용
- [ ] offer 생성 및 전달
- [ ] answer 생성 및 전달
- [ ] ICE candidate 송수신
- [ ] 마이크 on/off
- [ ] 카메라 on/off
- [ ] 화면 공유
- [ ] 연결 종료

## 7. 자주 막히는 문제와 해결 방법

### 카메라 권한이 안 뜨는 경우

원인:

- 브라우저 권한이 차단됨
- HTTP 환경에서 로컬이 아닌 주소로 접속함

해결:

- Chrome 사이트 설정에서 카메라/마이크 권한 초기화
- 개발 중에는 `localhost` 사용
- 배포 시 HTTPS 적용

### offer는 갔는데 영상이 안 나오는 경우

확인할 것:

- `addTrack()`을 offer 생성 전에 호출했는가
- `setLocalDescription()`과 `setRemoteDescription()` 순서가 맞는가
- `ontrack` 이벤트에서 `remoteVideo.srcObject`를 설정했는가

### ICE candidate 오류가 나는 경우

확인할 것:

- candidate를 상대방에게만 전달하고 있는가
- `setRemoteDescription()` 전에 candidate가 도착했는가
- remote description 설정 전 candidate를 임시 배열에 저장해야 하는 상황인가

### 같은 컴퓨터에서는 되는데 다른 컴퓨터에서는 안 되는 경우

원인:

- 방화벽
- 같은 네트워크가 아님
- HTTPS 문제
- TURN 서버 부재

해결:

- 같은 와이파이에서 테스트
- 로컬 IP와 포트 접근 허용
- 배포 환경에서는 HTTPS 적용
- 필요하면 TURN 서버 추가

## 8. 발표에 넣으면 좋은 화면

- 방 입장 화면
- 카메라/마이크 권한 요청 화면
- 두 브라우저 연결 화면
- 개발자 도구 콘솔의 offer / answer / ICE 로그
- 화면 공유 작동 화면
- 서버 콘솔의 join-room 로그

## 9. 최종 발표 스토리

1. WebRTC를 선택한 이유
2. 프로젝트 주제 소개
3. 전체 아키텍처 설명
4. signaling 서버 역할 설명
5. offer / answer / ICE candidate 흐름 설명
6. 구현 기능 시연
7. 어려웠던 점
8. 해결 방법
9. 개선 방향

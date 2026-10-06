// [클라이언트 1단계] Socket.IO 서버에 연결한다.
// 이 연결은 영상/음성 연결이 아니라 offer/answer/ICE를 주고받는 signaling 연결이다.
const socket = io();

// [클라이언트 2단계] HTML 요소를 JavaScript에서 사용할 수 있게 가져온다.
// id로 찾는 경우에는 querySelector("#id")보다 getElementById("id")가 설명하기 쉽다.
const joinForm = document.getElementById("joinForm");
const roomInput = document.getElementById("roomInput");
const nicknameInput = document.getElementById("nicknameInput");
const joinButton = document.getElementById("joinButton");

const localVideo = document.getElementById("localVideo");
const remoteVideo = document.getElementById("remoteVideo");

const micButton = document.getElementById("micButton");
const cameraButton = document.getElementById("cameraButton");
const screenButton = document.getElementById("screenButton");
const leaveButton = document.getElementById("leaveButton");

const roomLabel = document.getElementById("roomLabel");
const connectionLabel = document.getElementById("connectionLabel");
const iceLabel = document.getElementById("iceLabel");
const logList = document.getElementById("logList");

// [클라이언트 3단계] WebRTC 연결에 필요한 상태 값을 준비한다.
let roomId = "";
let localStream = null;
let remoteStream = null;
let peerConnection = null;
let cameraTrack = null;
let isMicOn = true;
let isCameraOn = true;

// setRemoteDescription()이 끝나기 전에 ICE candidate가 도착하는 경우가 있다.
// 그런 candidate는 잠시 저장해두었다가 remote description 설정 후 처리한다.
let pendingIceCandidates = [];

// [클라이언트 4단계] RTCPeerConnection에 사용할 ICE 서버 정보를 설정한다.
// STUN은 외부 주소 후보를 찾고, TURN은 직접 연결 실패 시 중계 후보를 만든다.
const rtcConfig = {
  // iceServers에 어떤 서버를 넣느냐에 따라 브라우저가 수집할 수 있는
  // ICE candidate 종류가 달라진다.
  //
  // - host: 내 기기의 로컬 네트워크 후보. 별도 서버 없이 자동 생성된다.
  // - srflx: STUN 서버를 통해 알게 된 외부 주소 후보.
  // - relay: TURN 서버를 통해 중계하는 후보.
  iceServers: [
    // STUN 서버는 브라우저가 외부에서 보이는 자신의 주소를 찾는 데 사용된다.
    // 과제/로컬 테스트에서는 공개 STUN 서버 하나로 충분한 경우가 많다.
    { urls: "stun:stun.l.google.com:19302" },

    // TURN 서버를 준비했다면 아래 설정을 추가한다.
    // TURN 설정이 있어야 relay candidate가 만들어질 수 있다.
    //
    {
      urls: "turn:222.108.163.174:3478",
      username: "turn-user",
      credential: "turn-password"
    }
  ]

  // 기본값은 "all"이다. host, srflx, relay 후보를 모두 시도한다.
  // relay 후보만 강제로 쓰고 싶으면 아래 옵션을 켠다.
  //
  // iceTransportPolicy: "relay"
};

// [클라이언트 5단계] 화면 로그와 디버깅용 보조 함수를 만든다.
/**
 * 화면 왼쪽의 연결 로그 영역에 메시지를 추가한다.
 *
 * WebRTC는 연결 순서가 중요하기 때문에, 스터디 중에는
 * 어떤 이벤트가 어떤 순서로 발생하는지 로그로 보는 것이 좋다.
 */
function addLog(message) {
  const item = document.createElement("li");
  item.textContent = message;
  logList.prepend(item);
}

/**
 * ICE candidate 문자열에서 후보 타입을 읽어온다.
 *
 * candidate 문자열 안에는 보통 "typ host", "typ srflx", "typ relay" 같은
 * 정보가 들어있다. 이 함수는 스터디 때 어떤 후보가 만들어졌는지
 * 로그로 확인하기 위해 사용한다.
 */
function getCandidateType(candidate) {
  if (!candidate || !candidate.candidate) {
    return "unknown";
  }

  const match = candidate.candidate.match(/ typ ([a-z]+)/);
  return match ? match[1] : "unknown";
}

/**
 * MediaStream 안의 트랙 상태를 로그로 출력한다.
 *
 * "내 목소리가 상대방에게 안 들림" 같은 문제를 찾을 때는
 * 오디오 트랙이 실제로 있는지, enabled/muted/readyState가 어떤지
 * 먼저 확인해야 한다.
 */
function logStreamTracks(stream, label) {
  const tracks = stream.getTracks();

  if (tracks.length === 0) {
    addLog(`${label}: 트랙이 없습니다.`);
    return;
  }

  tracks.forEach((track) => {
    addLog(
      `${label}: ${track.kind} 트랙, enabled=${track.enabled}, muted=${track.muted}, state=${track.readyState}`
    );
  });
}

// [클라이언트 6단계] 버튼 활성화/비활성화 보조 함수를 만든다.
/**
 * 통화 제어 버튼을 켜거나 끈다.
 *
 * 사용자가 방에 들어가기 전에는 마이크/카메라/화면 공유 버튼을
 * 누를 수 없게 막고, 방에 입장한 뒤에만 사용할 수 있게 한다.
 */
function setControlsEnabled(enabled) {
  micButton.disabled = !enabled;
  cameraButton.disabled = !enabled;
  screenButton.disabled = !enabled;
  leaveButton.disabled = !enabled;
}

// [클라이언트 7단계] 카메라와 마이크를 가져와 내 화면에 표시한다.
/**
 * 내 카메라와 마이크 스트림을 가져와 localVideo에 표시한다.
 *
 * getUserMedia()는 브라우저에 카메라/마이크 권한을 요청한다.
 * 성공하면 MediaStream을 반환하고, 이 스트림을 내 화면에 연결한다.
 */
async function startLocalMedia() {
  // getUserMedia()는 브라우저에게 카메라와 마이크 권한을 요청한다.
  localStream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: {
      echoCancellation: true,
      noiseSuppression: true,
      autoGainControl: true
    }
  });

  cameraTrack = localStream.getVideoTracks()[0];
  localVideo.srcObject = localStream;
  addLog("내 카메라/마이크 스트림을 가져왔습니다.");
  logStreamTracks(localStream, "내 로컬 스트림");

  localStream.getAudioTracks().forEach((track) => {
    track.onmute = () => {
      addLog("내 마이크 트랙이 mute 상태가 되었습니다.");
    };

    track.onunmute = () => {
      addLog("내 마이크 트랙이 다시 unmute 상태가 되었습니다.");
    };

    track.onended = () => {
      addLog("내 마이크 트랙이 종료되었습니다.");
    };
  });
}

// [클라이언트 8단계] RTCPeerConnection을 만들고 WebRTC 이벤트를 등록한다.
/**
 * WebRTC 연결 객체인 RTCPeerConnection을 생성한다.
 *
 * 이 함수에서 하는 일:
 * 1. RTCPeerConnection 생성
 * 2. 내 카메라/마이크 트랙을 연결에 추가
 * 3. ICE candidate 이벤트 등록
 * 4. 상대방 미디어 수신 이벤트 등록
 * 5. 연결 상태 변경 이벤트 등록
 */
function createPeerConnection() {
  if (peerConnection) {
    return peerConnection;
  }

  peerConnection = new RTCPeerConnection(rtcConfig);
  remoteStream = new MediaStream();
  remoteVideo.srcObject = remoteStream;

  // 내 카메라/마이크 트랙을 PeerConnection에 추가한다.
  // 이 작업을 해야 offer/answer SDP에 미디어 정보가 들어간다.
  localStream.getTracks().forEach((track) => {
    peerConnection.addTrack(track, localStream);
    addLog(`전송 트랙 추가: ${track.kind}, enabled=${track.enabled}`);
  });

  // WebRTC가 로컬 네트워크 후보를 찾을 때마다 실행된다.
  // 찾은 candidate는 signaling 서버를 통해 상대방에게 전달한다.
  peerConnection.onicecandidate = (event) => {
    if (!event.candidate) {
      addLog("ICE candidate 수집이 완료되었습니다.");
      return;
    }

    addLog(`내 ICE candidate 생성: ${getCandidateType(event.candidate)}`);

    socket.emit("ice-candidate", {
      roomId,
      candidate: event.candidate
    });
  };

  // 상대방이 보낸 영상/음성 트랙이 도착하면 remoteVideo에 붙인다.
  peerConnection.ontrack = (event) => {
    addLog(
      `상대방 ${event.track.kind} 트랙 수신: muted=${event.track.muted}, state=${event.track.readyState}`
    );

    event.streams[0].getTracks().forEach((track) => {
      remoteStream.addTrack(track);
    });

    addLog("상대방 미디어 트랙을 수신했습니다.");
  };

  // 연결 상태를 화면에 보여주면 발표 때 디버깅 흐름을 설명하기 좋다.
  peerConnection.onconnectionstatechange = () => {
    connectionLabel.textContent = peerConnection.connectionState;
    addLog(`PeerConnection 상태: ${peerConnection.connectionState}`);
  };

  peerConnection.oniceconnectionstatechange = () => {
    iceLabel.textContent = peerConnection.iceConnectionState;
    addLog(`ICE 연결 상태: ${peerConnection.iceConnectionState}`);
  };

  return peerConnection;
}

// [클라이언트 9단계] remote description보다 먼저 온 ICE candidate를 나중에 처리한다.
/**
 * 잠시 보관해둔 ICE candidate를 실제 PeerConnection에 추가한다.
 *
 * ICE candidate가 remote description보다 먼저 도착하면 바로 추가할 수 없다.
 * 그래서 pendingIceCandidates 배열에 넣어두었다가,
 * setRemoteDescription()이 끝난 뒤 이 함수에서 한 번에 처리한다.
 */
async function flushPendingIceCandidates() {
  if (!peerConnection || !peerConnection.remoteDescription) {
    return;
  }

  for (const candidate of pendingIceCandidates) {
    await peerConnection.addIceCandidate(candidate);
  }

  pendingIceCandidates = [];
}

// [클라이언트 10단계] 상대방이 들어오면 offer를 생성해서 보낸다.
/**
 * offer를 생성하고 signaling 서버를 통해 상대방에게 보낸다.
 *
 * 이 예제에서는 기존에 방에 있던 사용자가
 * 새 사용자가 들어왔다는 peer-joined 이벤트를 받으면 offer를 만든다.
 */
async function createAndSendOffer() {
  createPeerConnection();

  // offer는 통화를 시작하는 쪽이 만드는 연결 제안서다.
  const offer = await peerConnection.createOffer();
  await peerConnection.setLocalDescription(offer);

  socket.emit("offer", {
    roomId,
    offer
  });

  addLog("offer를 생성해 상대방에게 보냈습니다.");
}

// [클라이언트 11단계] offer를 받으면 answer를 만들어 보낸다.
/**
 * 상대방에게 받은 offer를 처리하고 answer를 만들어 보낸다.
 *
 * 처리 순서:
 * 1. 상대방 offer를 remote description으로 설정
 * 2. answer 생성
 * 3. answer를 local description으로 설정
 * 4. signaling 서버로 answer 전송
 */
async function handleOffer(offer) {
  createPeerConnection();

  // 상대방의 offer를 remote description으로 설정한다.
  await peerConnection.setRemoteDescription(offer);
  await flushPendingIceCandidates();

  // answer는 offer를 받은 쪽이 만드는 응답이다.
  const answer = await peerConnection.createAnswer();
  await peerConnection.setLocalDescription(answer);

  socket.emit("answer", {
    roomId,
    answer
  });

  addLog("offer를 받고 answer를 생성해 보냈습니다.");
}

// [클라이언트 12단계] 내가 보낸 offer에 대한 answer를 적용한다.
/**
 * 내가 보낸 offer에 대한 상대방의 answer를 적용한다.
 *
 * offer를 만든 쪽은 answer를 받아 remote description으로 설정해야
 * WebRTC의 미디어 조건 합의가 완료된다.
 */
async function handleAnswer(answer) {
  if (!peerConnection) {
    return;
  }

  // offer를 만든 쪽은 answer를 받아 remote description으로 설정한다.
  await peerConnection.setRemoteDescription(answer);
  await flushPendingIceCandidates();
  addLog("answer를 받아 연결 정보를 적용했습니다.");
}

// [클라이언트 13단계] 상대방 ICE candidate를 PeerConnection에 추가한다.
/**
 * 상대방에게 받은 ICE candidate를 PeerConnection에 추가한다.
 *
 * remote description이 아직 설정되지 않았다면 바로 추가하지 않고
 * pendingIceCandidates에 저장했다가 나중에 처리한다.
 */
async function handleIceCandidate(candidate) {
  if (!peerConnection) {
    pendingIceCandidates.push(candidate);
    return;
  }

  if (!peerConnection.remoteDescription) {
    pendingIceCandidates.push(candidate);
    return;
  }

  await peerConnection.addIceCandidate(candidate);
  addLog(`상대방 ICE candidate 추가: ${getCandidateType(candidate)}`);
}

// [클라이언트 14단계] 통화 종료 시 미디어 트랙을 중지하는 함수를 만든다.
/**
 * MediaStream 안의 모든 트랙을 중지한다.
 *
 * 카메라와 마이크는 브라우저 리소스를 사용하므로,
 * 방에서 나가거나 통화를 종료할 때 반드시 stop()으로 정리한다.
 */
function stopStream(stream) {
  if (!stream) {
    return;
  }

  stream.getTracks().forEach((track) => track.stop());
}

// [클라이언트 15단계] 통화 상태를 초기화하는 함수를 만든다.
/**
 * 통화 관련 상태를 처음 상태로 되돌린다.
 *
 * PeerConnection을 닫고, 미디어 트랙을 중지하고,
 * 화면과 버튼 상태를 입장 전 상태로 초기화한다.
 */
function resetCall() {
  if (peerConnection) {
    peerConnection.close();
  }

  peerConnection = null;
  remoteStream = null;
  pendingIceCandidates = [];

  stopStream(localStream);
  localStream = null;
  cameraTrack = null;

  localVideo.srcObject = null;
  remoteVideo.srcObject = null;

  setControlsEnabled(false);
  joinButton.disabled = false;
  roomLabel.textContent = "입장 전";
  connectionLabel.textContent = "대기 중";
  iceLabel.textContent = "대기 중";
}

// [클라이언트 16단계] 사용자가 방에 입장하는 흐름을 구현한다.
// 방 입장 버튼 클릭 → 카메라/마이크 가져오기 → signaling 서버에 join-room 전송.
joinForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  roomId = roomInput.value.trim();
  const nickname = nicknameInput.value.trim();

  if (!roomId) {
    alert("방 번호를 입력해주세요.");
    return;
  }

  try {
    joinButton.disabled = true;
    await startLocalMedia();

    socket.emit("join-room", {
      roomId,
      nickname
    });

    roomLabel.textContent = roomId;
    setControlsEnabled(true);
    addLog(`방 "${roomId}"에 입장 요청을 보냈습니다.`);
  } catch (error) {
    joinButton.disabled = false;
    addLog(`카메라/마이크 접근 실패: ${error.message}`);
    alert("카메라와 마이크 권한을 허용해주세요.");
  }
});

// [클라이언트 17단계] 통화 중 사용할 마이크/카메라/화면공유/나가기 버튼을 구현한다.
// 마이크 버튼을 누르면 오디오 트랙의 enabled 값을 바꾼다.
// 트랙을 제거하는 것이 아니라 잠시 끄는 방식이라 다시 켜기 쉽다.
micButton.addEventListener("click", () => {
  if (!localStream) {
    return;
  }

  isMicOn = !isMicOn;
  localStream.getAudioTracks().forEach((track) => {
    track.enabled = isMicOn;
  });

  micButton.textContent = isMicOn ? "마이크 끄기" : "마이크 켜기";
  addLog(isMicOn ? "마이크를 켰습니다." : "마이크를 껐습니다.");
});

// 카메라 버튼을 누르면 비디오 트랙의 enabled 값을 바꾼다.
// enabled가 false가 되면 상대방에게 검은 화면 또는 정지된 화면처럼 보일 수 있다.
cameraButton.addEventListener("click", () => {
  if (!localStream) {
    return;
  }

  isCameraOn = !isCameraOn;
  localStream.getVideoTracks().forEach((track) => {
    track.enabled = isCameraOn;
  });

  cameraButton.textContent = isCameraOn ? "카메라 끄기" : "카메라 켜기";
  addLog(isCameraOn ? "카메라를 켰습니다." : "카메라를 껐습니다.");
});

// 화면 공유 버튼을 누르면 getDisplayMedia()로 화면 스트림을 가져온다.
// 이후 replaceTrack()으로 기존 카메라 트랙을 화면 공유 트랙으로 교체한다.
screenButton.addEventListener("click", async () => {
  if (!peerConnection) {
    alert("상대방과 연결된 뒤 화면 공유를 시작할 수 있습니다.");
    return;
  }

  try {
    const screenStream = await navigator.mediaDevices.getDisplayMedia({
      video: true
    });

    const screenTrack = screenStream.getVideoTracks()[0];
    const videoSender = peerConnection
      .getSenders()
      .find((sender) => sender.track && sender.track.kind === "video");

    // replaceTrack()을 사용하면 offer/answer를 다시 만들지 않고
    // 전송 중인 비디오만 카메라에서 화면 공유로 바꿀 수 있다.
    await videoSender.replaceTrack(screenTrack);

    localVideo.srcObject = screenStream;
    screenButton.textContent = "화면 공유 중";
    addLog("화면 공유를 시작했습니다.");

    screenTrack.onended = async () => {
      await videoSender.replaceTrack(cameraTrack);
      localVideo.srcObject = localStream;
      screenButton.textContent = "화면 공유";
      addLog("화면 공유를 종료하고 카메라로 돌아왔습니다.");
    };
  } catch (error) {
    addLog(`화면 공유 실패: ${error.message}`);
  }
});

// 나가기 버튼을 누르면 서버에 방 나가기 이벤트를 보내고,
// 브라우저의 PeerConnection과 미디어 트랙도 함께 정리한다.
leaveButton.addEventListener("click", () => {
  socket.emit("leave-room");
  resetCall();
  addLog("방에서 나갔습니다.");
});

// [클라이언트 18단계] 서버에서 오는 signaling 이벤트를 처리한다.
// 여기서 offer, answer, ICE candidate를 받아 WebRTC 연결을 완성한다.
// Socket.IO 서버와 연결되었을 때 실행된다.
// 이 연결은 WebRTC 미디어 연결이 아니라 signaling 연결이다.
socket.on("connect", () => {
  addLog(`시그널링 서버에 연결되었습니다. socket id: ${socket.id}`);
});

// 서버가 방 입장을 승인하면 실행된다.
// 현재 방에 몇 명이 있는지 로그에 표시한다.
socket.on("room-joined", ({ memberCount }) => {
  addLog(`방 입장 완료. 현재 인원: ${memberCount}`);
});

// 같은 방에 상대방이 새로 들어오면 기존 사용자에게 전달되는 이벤트다.
// 이 이벤트를 받은 쪽이 offer를 만들어 WebRTC 연결을 시작한다.
socket.on("peer-joined", async () => {
  addLog("상대방이 입장했습니다. offer 생성을 시작합니다.");
  await createAndSendOffer();
});

// 상대방이 보낸 offer를 받으면 answer를 만들어 다시 보낸다.
socket.on("offer", async ({ offer }) => {
  addLog("상대방 offer를 받았습니다.");
  await handleOffer(offer);
});

// 내가 보낸 offer에 대한 상대방의 answer를 받으면 연결 정보에 적용한다.
socket.on("answer", async ({ answer }) => {
  addLog("상대방 answer를 받았습니다.");
  await handleAnswer(answer);
});

// 상대방이 보낸 ICE candidate를 받아 PeerConnection에 추가한다.
socket.on("ice-candidate", async ({ candidate }) => {
  await handleIceCandidate(candidate);
});

// 상대방이 나가면 remoteVideo를 비우고 연결 상태를 대기 상태로 바꾼다.
socket.on("peer-left", () => {
  addLog("상대방이 방을 나갔습니다.");

  if (peerConnection) {
    peerConnection.close();
    peerConnection = null;
  }

  remoteVideo.srcObject = null;
  remoteStream = null;
  connectionLabel.textContent = "상대방 나감";
  iceLabel.textContent = "대기 중";
});

// 서버가 방 인원 제한을 알리면 현재 통화 상태를 초기화한다.
socket.on("room-full", ({ message }) => {
  alert(message);
  addLog(message);
  resetCall();
});

// 방 번호가 없거나 입장 처리에 문제가 있을 때 실행된다.
socket.on("room-error", ({ message }) => {
  alert(message);
  addLog(message);
  resetCall();
});

// 브라우저 탭을 닫거나 새로고침할 때 서버에 방 나가기를 알려준다.
window.addEventListener("beforeunload", () => {
  socket.emit("leave-room");
});

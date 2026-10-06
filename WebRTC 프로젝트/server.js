// [서버 1단계] 필요한 라이브러리를 불러온다.
// express: HTML/CSS/JS 파일을 브라우저에 제공
// http: 실제 HTTP 서버 생성
// socket.io: WebRTC signaling 메시지를 실시간으로 전달
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");

// [서버 2단계] Express 앱을 HTTP 서버로 만들고 Socket.IO를 연결한다.
const app = express();
const server = http.createServer(app);
const io = new Server(server);

// [서버 3단계] 서버가 사용할 주소와 포트를 정한다.
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || "127.0.0.1";

// [서버 4단계] public 폴더의 정적 파일을 브라우저에 제공한다.
// public 폴더의 HTML, CSS, JS 파일을 브라우저에 제공한다.
app.use(express.static("public"));

// [서버 5단계] 방 정보를 저장할 메모리 저장소를 만든다.
// roomId -> Set(socketId)
// 발표 때 설명하기 좋도록 서버가 어떤 사용자를 어떤 방에 넣었는지 메모리에서 관리한다.
const rooms = new Map();

/*
  방 번호에 해당하는 참가자 목록을 가져온다.

  아직 만들어지지 않은 방이면 새 Set을 만들어 rooms에 저장한다.
  Set을 쓰는 이유는 같은 socket id가 중복으로 들어가는 것을 막기 위해서다.
-------------------------------------------------------------
  사용자가 방에 들어오려고 할 때,
  서버는 먼저 그 방이 이미 있는지 확인합니다.

  방이 없으면 새 방을 만들고,
  방이 있으면 그 방의 참가자 목록을 가져옵니다.

  그 다음 이 참가자 목록에 현재 사용자의 socket.id를 추가합니다.
 */
function getRoomMembers(roomId) {
  if (!rooms.has(roomId)) {
    rooms.set(roomId, new Set());
  }

  return rooms.get(roomId);
}

// [서버 6단계] 방에서 나가거나 접속이 끊겼을 때 정리하는 함수를 만든다.
/**
 * 사용자가 속한 모든 방에서 나가게 한다.
 *
 * 브라우저에서 나가기 버튼을 누르거나 탭을 닫으면 호출된다.
 * 남아 있는 상대방에게는 peer-left 이벤트를 보내서
 * 상대방 화면을 비우고 연결 상태를 갱신할 수 있게 한다.
 */
function leaveAllRooms(socket) {
  for (const [roomId, members] of rooms.entries()) {
    if (!members.has(socket.id)) {
      continue;
    }

    members.delete(socket.id);
    socket.to(roomId).emit("peer-left", { peerId: socket.id });

    if (members.size === 0) {
      rooms.delete(roomId);
    }

    console.log(`[leave-room] socket=${socket.id}, room=${roomId}`);
  }
}

// [서버 7단계] 브라우저가 Socket.IO로 접속하면 사용자별 이벤트를 등록한다.
io.on("connection", (socket) => {
  console.log(`[connection] socket=${socket.id}`);

  // [서버 8단계] 방 입장 이벤트를 처리한다.
  // 같은 roomId를 가진 사용자끼리만 signaling 메시지를 주고받게 한다.
  socket.on("join-room", ({ roomId, nickname }) => {
    if (!roomId) {
      socket.emit("room-error", { message: "방 번호가 필요합니다." });
      return;
    }

    const members = getRoomMembers(roomId);

    // 이 예제는 WebRTC 흐름을 이해하기 위한 1:1 통화 예제다.
    // 3명 이상은 SFU 또는 Mesh 구조가 필요하므로 여기서는 제한한다.
    if (members.size >= 2 && !members.has(socket.id)) {
      socket.emit("room-full", {
        message: "이 예제 방은 최대 2명까지만 입장할 수 있습니다."
      });
      return;
    }

    socket.join(roomId);
    members.add(socket.id);
    socket.data.roomId = roomId;
    socket.data.nickname = nickname || "익명";

    console.log(
      `[join-room] socket=${socket.id}, room=${roomId}, members=${members.size}`
    );

    socket.emit("room-joined", {
      roomId,
      peerId: socket.id,
      memberCount: members.size
    });

    // 이미 방에 있던 사용자에게 새 사용자가 들어왔음을 알려준다.
    // 이 알림을 받은 기존 사용자가 offer를 생성한다.
    socket.to(roomId).emit("peer-joined", {
      peerId: socket.id,
      nickname: socket.data.nickname
    });
  });

  // [서버 9단계] offer를 같은 방의 상대방에게 전달한다.
  // offer는 통화를 시작하는 쪽이 만드는 연결 제안서다.
  // 서버는 내용을 해석하지 않고 같은 방의 상대방에게 전달만 한다.
  socket.on("offer", ({ roomId, offer }) => {
    console.log(`[offer] from=${socket.id}, room=${roomId}`);
    socket.to(roomId).emit("offer", {
      peerId: socket.id,
      offer
    });
  });

  // [서버 10단계] answer를 같은 방의 상대방에게 전달한다.
  // answer는 offer를 받은 상대방이 만드는 응답이다.
  socket.on("answer", ({ roomId, answer }) => {
    console.log(`[answer] from=${socket.id}, room=${roomId}`);
    socket.to(roomId).emit("answer", {
      peerId: socket.id,
      answer
    });
  });

  // [서버 11단계] ICE candidate를 같은 방의 상대방에게 전달한다.
  // ICE candidate는 브라우저끼리 연결 가능한 네트워크 경로 후보이다.
  // 후보가 여러 개 생길 수 있으므로 연결 중 여러 번 전송된다.
  socket.on("ice-candidate", ({ roomId, candidate }) => {
    socket.to(roomId).emit("ice-candidate", {
      peerId: socket.id,
      candidate
    });
  });

  // [서버 12단계] 사용자가 직접 나가기 버튼을 누른 경우를 처리한다.
  socket.on("leave-room", () => {
    leaveAllRooms(socket);
  });

  // [서버 13단계] 브라우저 종료/새로고침/네트워크 끊김을 처리한다.
  socket.on("disconnect", () => {
    leaveAllRooms(socket);
    console.log(`[disconnect] socket=${socket.id}`);
  });
});

// [서버 14단계] 서버 실행 중 발생할 수 있는 대표 에러를 처리한다.
server.on("error", (error) => {
  if (error.code === "EADDRINUSE") {
    console.error(
      `포트 ${PORT}번이 이미 사용 중입니다. 기존 서버를 종료하거나 PORT=3001 npm start처럼 다른 포트로 실행해주세요.`
    );
    process.exit(1);
  }

  throw error;
});

// [서버 15단계] HTTP + Socket.IO 서버를 실행한다.
server.listen(PORT, HOST, () => {
  console.log(`WebRTC study room server running on http://${HOST}:${PORT}`);
});

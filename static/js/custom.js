var websocket;
window.addEventListener("load", onLoad);

function onLoad() {
  initializeSocket();
  setDefaultSpeed();
}

function initializeSocket() {
  console.log(
    "Opening WebSocket connection to Raspberry Pi MicroPython Server..."
  );
  var targetUrl = `ws://${location.host}/ws`;
  websocket = new WebSocket(targetUrl);
  websocket.onopen = onOpen;
  websocket.onclose = onClose;
  websocket.onmessage = onMessage;
  websocket.onerror = onError;
}
function onOpen(event) {
  console.log("Starting connection to WebSocket server..");
}
function onClose(event) {
  console.log("Closing connection to server..");
  setTimeout(initializeSocket, 2000);
}
function onMessage(event) {
  console.log("WebSocket message received:", event);
}
function onError(event) {
  console.log(
    "Error encountered while communicating with WebSocket server..",
    event
  );
}

function sendMessage(message) {
  websocket.send(message);
}

/*
Speed Settings Handler
*/
const speed = document.querySelector("#currentSpeed");
const speedValue = document.querySelector("#speedValue");

speed.addEventListener("input", () => {
  speedValue.innerHTML = speed.value;
  sendMessage("speed : " + speed.value);
});
// var speedSettings = document.querySelectorAll(
//   'input[type=radio][name="speed-settings"]'
// );
// speedSettings.forEach((radio) =>
//   radio.addEventListener("change", () => {
//     var speedSettings = radio.value;
//     console.log("Speed Settings :: " + speedSettings);
//     sendMessage(speedSettings);
//   })
// );

function setDefaultSpeed() {
  // console.log("Setting default speed to normal..");
  // let normalOption = document.getElementById("option-2");
  // normalOption.checked = true;
}

/*
O-Pad/ D-Pad Controller and Javascript Code
*/
// Prevent scrolling on every click!
// super sweet vanilla JS delegated event handling!
document.body.addEventListener("click", function (e) {
  if (e.target && e.target.nodeName == "A") {
    e.preventDefault();
  }
});

function touchStartHandler(event) {
  var direction = event.target.dataset.direction;
  console.log("Touch Start :: " + direction);
  sendMessage(direction);
}

function touchEndHandler(event) {
  const stop_command = "stop";
  var direction = event.target.dataset.direction;
  console.log("Touch End :: " + direction);
  sendMessage(stop_command);
}

document.querySelectorAll(".control").forEach((item) => {
  item.addEventListener("touchstart", touchStartHandler);
});

document.querySelectorAll(".control").forEach((item) => {
  item.addEventListener("touchend", touchEndHandler);
});
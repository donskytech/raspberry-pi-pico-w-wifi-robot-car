from microdot_asyncio import Microdot, Response, send_file
from microdot_asyncio_websocket import with_websocket
from microdot_utemplate import render_template
from robot_car import RobotCar

app = Microdot()
Response.default_content_type = "text/html"

# Pico W GPIO Pin
LEFT_MOTOR_PIN_1 = 16
LEFT_MOTOR_PIN_2 = 17
RIGHT_MOTOR_PIN_1 = 18
RIGHT_MOTOR_PIN_2 = 19

motor_pins = [LEFT_MOTOR_PIN_1, LEFT_MOTOR_PIN_2, RIGHT_MOTOR_PIN_1, RIGHT_MOTOR_PIN_2]

# Create an instance of our robot car
robot_car = RobotCar(motor_pins, 20000)

car_commands = {
    "forward": robot_car.move_forward,
    "reverse": robot_car.move_backward,
    "left": robot_car.turn_left,
    "right": robot_car.turn_right,
    "stop": robot_car.stop,
}


# App Route
@app.route("/")
async def index(request):
    print(f"Current Speed: {robot_car.get_current_speed()}")
    return render_template("index.html", current_speed=robot_car.get_current_speed())


@app.route("/ws")
@with_websocket
async def executeCarCommands(request, ws):
    while True:
        websocket_message = await ws.receive()

        if "speed" in websocket_message:
            # WebSocket message format: "speed : 20"
            speedMessage = websocket_message.split(":")
            robot_car.change_speed(speedMessage[1])
        else:
            command = car_commands.get(websocket_message)
            if command is not None:
                command()
        ws.send("OK")


@app.route("/shutdown")
async def shutdown(request):
    request.app.shutdown()
    return "The server is shutting down..."


@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)


if __name__ == "__main__":
    try:
        app.run()
    except KeyboardInterrupt:
        robot_car.deinit()

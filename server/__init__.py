import flask as f
from server.remotes import REMOTES

app = f.Flask(__name__)


@app.route("/<string:remote>/<string:command>/", methods=["POST"])
def send_command(remote: str, command: str):
    app.logger.log(1, f"remote: {remote}, command: {command}")
    REMOTES[remote.replace("+", " ")].send(command.replace("+", " "))
    return 200


@app.route("/macro/<string:name>", methods=['POST'])
def send_macro(name):
    pass
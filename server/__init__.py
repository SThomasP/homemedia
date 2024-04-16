import flask as f
from server.remotes import send

app = f.Flask(__name__)


@app.route("/<string:remote>/<string:command>/", methods=["POST"])
def send_command(remote: str, command: str):
    send(remote, command)
    return "success",  200


@app.route("/macro/<string:name>", methods=['POST'])
def send_macro(name):
    pass
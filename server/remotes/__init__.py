from importlib import resources
from .remote import Remote

IR_OUT_PIN = 17
REMOTES = {}

for file in resources.files("server.remotes").iterdir():
    if file.is_file() and file.name.endswith(".json"):
        filename = file.name.rsplit(".", 1)[0]
        with file.open("r") as path:
            remote = Remote(path, IR_OUT_PIN)
            REMOTES[filename] = remote

def send(remote_name, command):
    REMOTES[remote_name].send(command)

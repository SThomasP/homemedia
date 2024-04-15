import piir
from importlib import resources
IR_OUT_PIN = 17
REMOTES = {}
for file in resources.files("server.remotes").iterdir():
    if file.is_file() and file.name.endswith(".json"):
        filename = file.name.rsplit(".", 1)[0]
        with file.open("r") as path:
            remote = piir.Remote(path, IR_OUT_PIN)
            REMOTES[filename] = remote

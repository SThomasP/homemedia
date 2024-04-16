import json
from piir import Remote as PiRemote

DEBUG = True


class TestRemote:
    def __init__(self, path, _):
        self.keys = json.load(path)['keys']

    def send(self, key, repeat=1):
        if key in self.keys:
            print(f"sending {key} {repeat} times")


if DEBUG:
    Remote = TestRemote
else:
    Remote = PiRemote

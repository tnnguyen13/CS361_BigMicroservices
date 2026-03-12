"""
Climbing Log Microservice
"""

import zmq
import json

class ClimbingLogClient:
    def __init__(self, address: str = "tcp://localhost:5555"):
        self.address = address
        self._ctx = zmq.Context()
        self._sock = None

    def connect(self):
        self._sock = self._ctx.socket(zmq.REQ)
        self._sock.connect(self.address)
        return self

    def close(self):
        if self._sock:
            self._sock.close()
        self._ctx.term()

    def __enter__(self):
        return self.connect()

    def __exit__(self, *_):
        self.close()

    def _send(self, action: str, data: dict = {}) -> dict:
        if not self._sock:
            raise RuntimeError("Not connected")
        self._sock.send(json.dumps({"action": action, "data": data}).encode())
        return json.loads(self._sock.recv())

    def add(self, username: str, route: str, grade: int, rating: str, *, location="", attempts=1, notes="", date="") -> dict:
        payload = {"username": username, "route": route, "grade": grade, "rating": rating,
                   "location": location, "attempts": attempts, "notes": notes}
        if date:
            payload["date"] = date
        return self._send("add", payload)

    def get(self, username: str, climb_id: int) -> dict:
        return self._send("get", {"username": username, "id": climb_id})

    def list(self, username: str, *, grade="", rating="", location="") -> dict:
        filters = {k: v for k, v in {"grade": grade, "rating": rating, "location": location}.items() if v}
        return self._send("list", {"username": username, **filters})

# sample runs
if __name__ == "__main__":
    with ClimbingLogClient() as client:
        client.add("tee", "Life's Porpoise", "v3", 8, location="Carmel Meadows")
        client.add("tee", "The Crack", "v2", 7, location="Castle Rock")
        client.add("tee", "The Slap", "v5", 10, location="Castle Rock")
        print(client.list("tee"))
        client.add("sylvia", "Moonlight Sonata", "v16", 10, location="Joe's Valley")
        print(client.list("sylvia"))

"""
zeromq set up and dispatching for climbing log microservice.
"""

import zmq
import json
from database import init_db
from handlers import HANDLERS


def dispatch(raw: bytes) -> bytes:
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        print("Invalid JSON received")
        return json.dumps({}).encode()
    action = msg.get("action", "")
    handler = HANDLERS.get(action)
    if not handler:
        print(f"Unknown action: {action}")
        return json.dumps({}).encode()
    return json.dumps(handler(msg.get("data", {}))).encode()


def main(port: int = 5555):
    init_db()
    ctx = zmq.Context()
    sock = ctx.socket(zmq.REP)
    sock.bind(f"tcp://*:{port}")
    print(f"Climbing log server listening on tcp://localhost:{port}")
    try:
        while True:
            raw = sock.recv()
            sock.send(dispatch(raw))
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        sock.close()
        ctx.term()


if __name__ == "__main__":
    main()

from flask_socketio import SocketIO


socketio = SocketIO()


@socketio.on("connect")
def _connect():
    print("connected")
    

class EventStore:

    @staticmethod
    def dbin_filled(data):
        print("dbin_filled emited")
        socketio.emit("dbin_filled", data)

    @staticmethod
    def dbin_emptied(data):
        socketio.emit("dbin_emptied", data)



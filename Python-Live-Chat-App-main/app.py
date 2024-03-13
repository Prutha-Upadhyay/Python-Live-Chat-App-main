


# from flask import Flask, render_template, request, session, redirect, url_for
# from flask_socketio import join_room, leave_room, send, SocketIO
# from flask_sqlalchemy import SQLAlchemy
# import random
# import string


# app = Flask(__name__)




# # Create a Flask application context


# app.secret_key = "hjhjsdahhds"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatrooms.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # SQLite database URI
# db = SQLAlchemy(app)
# socketio = SocketIO(app)

# class ChatRoom(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     room_id = db.Column(db.String(10), unique=True, nullable=False)
#     password = db.Column(db.String(50), nullable=False)

#     def __repr__(self):
#         return f"ChatRoom(name={self.name}, room_id={self.room_id})"

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     room_id = db.Column(db.String(10), nullable=False)
#     sender_name = db.Column(db.String(50), nullable=False)
#     message = db.Column(db.String(500), nullable=False)

#     def __repr__(self):
#         return f"Message(room_id={self.room_id}, sender_name={self.sender_name}, message={self.message})"

# with app.app_context():
#     # Create all tables
#     db.create_all()


# @app.route("/", methods=["POST", "GET"])
# def home():
#     session.clear()
#     error = None
#     if request.method == "POST":
#         name = request.form.get("name")
#         password = request.form.get("password")
#         join = request.form.get("join", False)
#         create = request.form.get("create", False)

#         if not name:
#             error = "Please enter a name."
#         elif join:
#             code = request.form.get("room_id")
#             chatroom = ChatRoom.query.filter_by(room_id=code).first()
#             if not chatroom or chatroom.password != password:
#                 error = "Invalid room code or password."
#             else:
#                 session["room"] = chatroom.room_id
#                 session["name"] = name
#                 return redirect(url_for("room"))
#         elif create:
#             room_name = request.form.get("room_name")
#             if not room_name:
#                 error = "Please enter a room name."
#             else:
#                 room_id = ''.join(random.choices(string.ascii_uppercase, k=6))
#                 chatroom = ChatRoom(name=room_name, room_id=room_id, password=password)
#                 db.session.add(chatroom)
#                 db.session.commit()
#                 session["room"] = chatroom.room_id
#                 session["name"] = name
#                 return redirect(url_for("room"))
#         else:
#             error = "Please select either join or create a room."
    
#     chatrooms = ChatRoom.query.all()
#     return render_template("home.html", error=error, chatrooms=chatrooms)

# @app.route("/room")
# def room():
#     room_id = session.get("room")
#     name = session.get("name")
#     if not room_id or not name:
#         return redirect(url_for("home"))
    
#     messages = Message.query.filter_by(room_id=room_id).all()
#     return render_template("room.html", room_id=room_id, name=name, messages=messages)

# @socketio.on("message")
# def message(data):
#     room_id = session.get("room")
#     name = session.get("name")
#     if not room_id or not name:
#         return 
    
#     message = Message(room_id=room_id, sender_name=name, message=data["data"])
#     db.session.add(message)
#     db.session.commit()
#     send({"name": name, "message": message.message}, to=room_id)

# @socketio.on("connect")
# def connect(auth):
#     room_id = session.get("room")
#     name = session.get("name")
#     if not room_id or not name:
#         return
    
#     join_room(room_id)
#     send({"name": name, "message": "has entered the room"}, to=room_id)

# @socketio.on("disconnect")
# def disconnect():
#     room_id = session.get("room")
#     name = session.get("name")
#     if room_id:
#         leave_room(room_id)
#         send({"name": name, "message": "has left the room"}, to=room_id)

# if __name__ == "__main__":
#     socketio.run(app, debug=True)


# from flask import Flask, render_template, request, session, redirect, url_for
# from flask_socketio import join_room, leave_room, send, SocketIO
# from flask_sqlalchemy import SQLAlchemy
# import random
# import string

# app = Flask(__name__)
# app.secret_key = "hjhjsdahhds"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatrooms.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
# socketio = SocketIO(app)

# class ChatRoom(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     room_id = db.Column(db.String(10), unique=True, nullable=False)
#     password = db.Column(db.String(50), nullable=False)

#     def __repr__(self):
#         return f"ChatRoom(name={self.name}, room_id={self.room_id})"

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     room_id = db.Column(db.String(10), nullable=False)
#     sender_name = db.Column(db.String(50), nullable=False)
#     message = db.Column(db.String(500), nullable=False)

#     def __repr__(self):
#         return f"Message(room_id={self.room_id}, sender_name={self.sender_name}, message={self.message})"

# with app.app_context():
#     db.create_all()

# @app.route("/", methods=["GET", "POST"])
# def home():
#     session.clear()
#     error = None
#     chatrooms = ChatRoom.query.all()
#     if request.method == "POST":
#         name = request.form.get("name")
#         if not name:
#             error = "Please enter a name."
#         else:
#             action = request.form.get("action")
#             if action == "create":
#                 return redirect(url_for("create_room"))
#             elif action == "join":
#                 return redirect(url_for("join_room"))

#     return render_template("home.html", error=error, chatrooms=chatrooms)

# @app.route("/create-room", methods=["GET", "POST"])
# def create_room():
#     error = None
#     if request.method == "POST":
#         name = request.form.get("name")
#         password = request.form.get("password")
#         room_name = request.form.get("room_name")

#         if not name or not room_name or not password:
#             error = "Please fill out all fields."
#         else:
#             room_id = ''.join(random.choices(string.ascii_uppercase, k=6))
#             chatroom = ChatRoom(name=room_name, room_id=room_id, password=password)
#             db.session.add(chatroom)
#             db.session.commit()
#             session["room"] = chatroom.room_id
#             session["name"] = name
#             return redirect(url_for("room"))

#     return render_template("create_room.html", error=error)

# @app.route("/join-room", methods=["GET", "POST"])
# def join_room():
#     error = None
#     if request.method == "POST":
#         name = request.form.get("name")
#         password = request.form.get("password")
#         code = request.form.get("room_id")

#         if not name or not code or not password:
#             error = "Please fill out all fields."
#         else:
#             chatroom = ChatRoom.query.filter_by(room_id=code).first()
#             if not chatroom or chatroom.password != password:
#                 error = "Invalid room code or password."
#             else:
#                 session["room"] = chatroom.room_id
#                 session["name"] = name
#                 return redirect(url_for("room"))

#     return render_template("join_room.html", error=error)

# @app.route("/room")
# def room():
#     room_id = session.get("room")
#     name = session.get("name")
#     if not room_id or not name:
#         return redirect(url_for("home"))

#     messages = Message.query.filter_by(room_id=room_id).all()
#     return render_template("room.html", room_id=room_id, name=name, messages=messages)

# @socketio.on("message")
# def message(data):
#     room_id = session.get("room")
#     name = session.get("name")
#     if not room_id or not name:
#         return

#     message = Message(room_id=room_id, sender_name=name, message=data["data"])
#     db.session.add(message)
#     db.session.commit()
#     send({"name": name, "message": message.message}, to=room_id)

# @socketio.on("connect")
# def connect(auth):
#     room_id = session.get("room")
#     name = session.get("name")
#     if not room_id or not name:
#         return

#     join_room(room_id)
#     send({"name": name, "message": "has entered the room"}, to=room_id)

# @socketio.on("disconnect")
# def disconnect():
#     room_id = session.get("room")
#     name = session.get("name")
#     if room_id:
#         leave_room(room_id)
#         send({"name": name, "message": "has left the room"}, to=room_id)

# if __name__ == "__main__":
#     socketio.run(app, debug=True)


from datetime import datetime
import re
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_sqlalchemy import SQLAlchemy

import random
import string

app = Flask(__name__)
app.secret_key = "hjhjsdahhds"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatrooms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)



class ChatRoom(db.Model):
    id = db.Column(db.Integer,autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    room_id = db.Column(db.String(10), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"ChatRoom(name={self.name}, room_id={self.room_id})"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(10), nullable=False)
    sender_name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Add this line

    def __repr__(self):
        return f"Message(room_id={self.room_id}, sender_name={self.sender_name}, message={self.message})"

with app.app_context():
    db.create_all()
    # Check if there are existing rooms in the database
    if ChatRoom.query.count() == 0:
        # If no rooms exist, initialize the room ID counter to 1
        room_id_counter = 1
    else:
        # If rooms exist, find the maximum room ID and set the counter to 1 more than that
        max_room_id = ChatRoom.query.order_by(ChatRoom.room_id.desc()).first().room_id
        room_id_counter = int(max_room_id) + 1


@app.route("/", methods=["GET", "POST"])
def home():
    session.clear()
    error = None
    chatrooms = ChatRoom.query.all()
    action = request.args.get("action")

    if action == "create":
        return redirect(url_for("create_room"))
    elif action == "join":
        return redirect(url_for("join_chatroom"))

    return render_template("home.html", error=error, chatrooms=chatrooms)



@app.route("/create-room", methods=["GET", "POST"])
def create_room():
    global room_id_counter
    error = None
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        room_name = request.form.get("room_name")

        if not name or not room_name or not password:
            error = "Please fill out all fields."
        else:
            # room_id = random.randint(100, 999999) 
            # chatroom = ChatRoom(name=room_name, room_id=room_id, password=password)
            # db.session.add(chatroom)
            # db.session.commit()
            # session["room"] = chatroom.room_id
            # session["name"] = name
            # return redirect(url_for("room"))

            chatroom = ChatRoom(name=room_name, room_id=room_id_counter, password=password)
            db.session.add(chatroom)
            db.session.commit()
            session["room"] = chatroom.room_id
            session["name"] = name
            session["room_name"] = chatroom.name
            # Increment the room ID counter for the next room
            room_id_counter += 1
            return redirect(url_for("room"))

    return render_template("create_room.html", error=error)

@app.route("/join-room", methods=["GET", "POST"])
def join_chatroom():
    error = None
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        code = request.form.get("room_id")
        # room_name = request.form.get("room_name")

        if not name or not code or not password:
            error = "Please fill out all fields."
        else:
            chatroom = ChatRoom.query.filter_by(room_id=code).first()
            if not chatroom or chatroom.password != password:
                error = "Invalid room code or password."
            else:
                session["room"] = chatroom.room_id
                session["name"] = name
                session["room_name"] = chatroom.name
                return redirect(url_for("room"))

    return render_template("join_room.html", error=error)

@app.route("/room")
def room():
    room_id = session.get("room")
    name = session.get("name")
    room_name = session.get("room_name")
    if not room_id or not name:
        return redirect(url_for("home"))

    messages = Message.query.filter_by(room_id=room_id).all()
    return render_template("room.html", code=room_id, messages=messages,room_name=room_name)


@socketio.on("message")
def message(data):
    room_id = session.get("room")
    name = session.get("name")
    if not room_id or not name:
        return
    
    message = Message(room_id=room_id, sender_name=name, message=data["data"])
    db.session.add(message)
    db.session.commit()
    send({"name": name, "message": message.message}, to=room_id)


@socketio.on("connect")
def connect():
    room_id = session.get("room")
    name = session.get("name")
    if not room_id or not name:
        return

    join_room(room_id)
    session["name"] = name
    send({"name": name, "message": "has entered the room"}, to=room_id)


@socketio.on("disconnect")
def disconnect():
    room_id = session.get("room")
    name = session.get("name")
    if room_id:
        leave_room(room_id)
        send({"name": name, "message": "has left the room"}, to=room_id)


if __name__ == "__main__":
    socketio.run(app, debug=True)
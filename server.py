#!chattty/bin/python 
from flask import Flask, render_template, session, request, jsonify
from flask.ext.socketio import SocketIO, emit, join_room
import eventlet

eventlet.monkey_patch()
 
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super_secret'
socketio = SocketIO(app)
rooms = [
	{
        'id': 0,
        'title': u'default'
    },
    {
        'id': 1,
        'title': u'ser'
    },
    {
        'id': 2,
        'title': u'jaks'
       
    },
    {
        'id': 3,
        'title': u'tesSS'
       
    }
]

@app.route('/')
def chat():
    return render_template('chat.html')
 
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/rooms')
def get_rooms():
	return jsonify({'rooms' : rooms})

@socketio.on('join')
def on_join(data):
	username = data['username']
	room = data['room']
	join_room(room)
	send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
	username = data['username']
	room = data['room']
	leave_room(room)
	send(username + ' has left the room.', room=room)

@socketio.on('message', namespace='/chat')
def chat_message(message):
	emit('message', {'data': message['data']}, broadcast = True)
 
@socketio.on('connected', namespace='/chat')
def connected_user(message):
    emit('addToUserList', {'data': message['data']}, broadcast = True)

@socketio.on('disconnect', namespace='/chat')
def connected_user(message):
    emit('removeFromUserList', {'data': message['data']}, broadcast = True)
 
 
if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=5000)

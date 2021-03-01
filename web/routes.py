from flask import render_template, request, Response, send_from_directory, jsonify #url_for
from web import app , db
from web.models import ClassFactory
from flask_migrate import upgrade, migrate, init
import os, signal

f = "./room.tmp"
tables = {}
db_status = {}
db_status['version'] = 'build_number'

def shutdown_server():
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
    raise RuntimeError('Not running with the Werkzeug Server')
  func()

def create_table_instance(room):
  if room not in tables:
    tables[room] = ClassFactory(room)

def write_2_file(room):
  with open(f,"w+") as file:
    if room not in db.engine.table_names():
      file.write("No chat history")
    else:
      for p in tables[room].query.order_by(db.desc(tables[room].id)).all():
        file.write("[{}] {}: {}\n".format(p.timestamp, p.username, p.messages))

def db_health():
  try:
    db.session.query("1").all()
    db_status['status'] = 'ok'
  except:
    db_status['status'] = 'DB connection lost'
  return db_status

@app.route('/stopServer', methods=['GET'])
def stopServer():
  shutdown_server()
  os.kill(os.getpid(), signal.SIGINT)
  return jsonify({ "success": True, "message": "Server is shutting down..." })

@app.route('/healthz')
def healthz():
  return (res := db_health()), 400 if 'lost' in res['status'] else res

@app.route('/')
@app.route('/<room>')
def room(room=None):
  print(room)
  return send_from_directory('static', 'index.html')

@app.route('/api/chat/<room>', methods=['GET', 'POST'])
@app.route('/api/chat/', methods=['GET', 'POST'])
def data(room='general'):
  if 'lost' in (res := db_health())['status']: return res, 400
  create_table_instance(room)
  if request.method == 'POST':
    if room not in db.engine.table_names():
      migrate(message='Added room {}'.format(room))
      upgrade()
    post = tables[room](username=request.form.get('username'), messages=request.form.get('msg'))
    db.session.add(post)
    db.session.commit()

  write_2_file(room)
  with open(f, "r") as file:
    content = file.read()
  return Response(content, mimetype='text/plain')

@app.route('/chat/<room>')
@app.route('/chat/')
def display(room='general'):
  if 'lost' in (res := db_health())['status']: return res, 400
  create_table_instance(room)
  write_2_file(room)
  messages = []
  with open(f, "r") as file:
     for line in file.readlines():
        messages.append(line.rstrip())
  return render_template('data.html', room=room, messages=messages)

from datetime import datetime, timezone
from web import db

def time():
  return datetime.now(timezone.utc).replace(microsecond=0)
  # .strftime("%Y-%m-%d %H:%M:%S") #to string date time format

def ClassFactory(name):
  tabledict={'id':db.Column(db.Integer, primary_key = True),
              'timestamp':db.Column(db.DateTime, index=True, default=time),
              'username':db.Column(db.String(64), index=True),
              'messages':db.Column(db.String(256), index=True),}
            
  return type(name, (db.Model,), tabledict)

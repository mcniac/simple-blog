import os, urlparse
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from mongoengine import connect
from flask.ext.markdown import Markdown

# import settings

app = Flask(__name__)
app.debug = True
app.config["MONGODB_DB"] = "my_tumble_log"
app.config["SECRET_KEY"] = "KeepThisS3cr3t"


Markdown(app)

MONGOLAB_URI = os.environ.get('MONGOLAB_URI')
if MONGOLAB_URI:
    url = urlparse.urlparse(MONGOLAB_URI)
    app.config["MONGODB_SETTINGS"] = {
        'db': url.path[1:],
        'username': url.username,
        'password': url.password,
        'host': url.hostname,
        'port': url.port
    }
    app.config["MONGODB_DB"] = url.path[1:]

# 

# ToDo add markdown support and embed urls

db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from tumblelog.views import posts
    from tumblelog.admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)
    
register_blueprints(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port)

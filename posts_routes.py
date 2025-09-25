from flask import request, jsonify
from flask_smorest import Blueprint, abort

def create_posts_blueprint(mysql):
    create_blp = Blueprint("posts", __name__, description='posts api')
    

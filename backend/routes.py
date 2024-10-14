from app import app,db
from flask import request, jsonify
from models import Dost

@app.route("/api/friends",methods=["GET"])
def get_friends():
    friends = Dost.queryall() 
    result = [friend.to_json() for friend in friends]
    return jsonify
    
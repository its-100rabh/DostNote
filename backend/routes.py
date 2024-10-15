from app import app,db
from flask import request, jsonify
from models import Dost

@app.route("/api/friends",methods=["GET"]) #Get all friends
def get_friends():
    friends = Dost.query.all() 
    result = [friend.to_json() for friend in friends]
    return jsonify(result)
    
    
#create a friend
@app.route("/api/friends",methods=["POST"])
def create_friend():
    try:
        data = request.json
        
        required_fields = ["name","role","description","gender"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error":f'Missing required field: {field}'}),400
        
        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")
        
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None 
            
        new_friend = Dost(name = name , role = role, description = description, gender = gender, img_url = img_url)
        db.session.add(new_friend) #not immediately add
        db.session.commit()
        return jsonify({"msg":"Dost Created Successfully"}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500
    
#delete a friend
@app.route("/api/friends/<int:id>",methods=["DELETE"])
def delete_friend(id):
    try:
        friend = Dost.query.get(id)
        if friend is None:
            return jsonify({"error":"Dost not found"}),404
        db.session.delete(friend)
        db.session.commit()
        return jsonify({"msg":"Dost Deleted from life"}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

#update a friend
@app.route("/api/friends/<int:id>",methods=["PATCH"])
def update_friend(id):
    try:
        friend = Dost.query.get(id)
        if friend is None:
            return jsonify({"error":"Dost not found"}),404
        data = request.json
        friend.name = data.get("name",friend.name)
        friend.role = data.get("role",friend.role)
        friend.description = data.get("description",friend.description)
        friend.gender = data.get("gender",friend.gender)
        
        db.session.commit()
        return jsonify(friend.to_json()),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500
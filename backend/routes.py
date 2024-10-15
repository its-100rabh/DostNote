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
from flask import Flask , request , render_template , jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["flask_assigment"]
collection = db["todo_items"]

@app.route('/submittodoitem', methods=['POST'])
def submit ():

    item_name = request.form.get('itemName', '').strip()
    item_description = request.form.get('itemDescription', '').strip()

    if not item_name or not item_description:
        return jsonify({
            "error": "Item name and description are required"
        }), 400

    try:
        collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })

        return jsonify({
            "message": "To-Do item saved sucessfully"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
   

if __name__ == '__main__' : 
    app.run(debug=True)
from flask import Flask , jsonify , request , render_template , redirect , url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")


client = MongoClient(MONGO_URI)

db = client["flask_assignment"]
collection = db["users"]

try:
    client.admin.command("ping")
    print("MongoDB connnected successfully")
except Exception as e:
    print("MongoDB connection failed",e)



@app.route('/')
def home():

    return render_template('index.html')



@app.route('/api/users' , methods=['POST'])
def add_user():

    data = {
        "name": request.form.get('name').strip(),
        "email": request.form.get('email').strip(),
        "role": request.form.get('role').strip()
    }

    if not all(data.values()):
        return render_template(
            'index.html',
            error= "All fields are required."
        ), 400

  

    try:
        collection.insert_one(data)
        return redirect(url_for('success'))


    except Exception as e:
        return render_template(
            'index.html',
            error=f"Database error: {e}"
        ), 500

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':

    app.run(debug=True)


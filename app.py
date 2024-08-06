from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"

def dockerMongoDB():
    client = MongoClient(host='test_mongodb',
                        port=27017, 
                        username='root', 
                        password='pass',
                        authSource="admin")
    db = client.users
    pw = "test123"
    hashed = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
    records = db.register
    records.insert_one({
        "name": "Test Test",
        "email": "test@yahoo.com",
        "password": hashed
    })
    return records

records = dockerMongoDB()

@app.route("/users", methods=['GET'])
def list_users():
    users = records.find()
    users_list = [{'name': user['name'], 'email': user['email']} for user in users]
    return jsonify(users_list)

@app.route("/users", methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password1 = data.get('password1')
    password2 = data.get('password2')

    if not name or not email or not password1 or not password2:
        return jsonify({"error": "Nome, email e senhas são obrigatórios!"}), 400

    if password1 != password2:
        return jsonify({"error": "As senhas devem corresponder!"}), 400

    if records.find_one({"name": name}) or records.find_one({"email": email}):
        return jsonify({"error": "Usuário ou email já existe!"}), 400

    hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
    user_input = {'name': name, 'email': email, 'password': hashed}
    records.insert_one(user_input)
    
    return jsonify({"message": "Usuário adicionado com sucesso!"}), 201

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

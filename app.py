from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

def dockerMongoDB():
    client = MongoClient(host='test_mongodb',
                        port=27017, 
                        username='root', 
                        password='pass',
                        authSource="admin")
    db = client.consultas
    return db.registros

consultas = dockerMongoDB()

@app.route("/consultas", methods=['GET'])
def listar_consultas():
    # Lista todas as consultas
    consultas_lista = list(consultas.find({}, {'_id': 0}))  
    return jsonify(consultas_lista)

@app.route("/consultas", methods=['POST'])
def cadastrar_consulta():
    data = request.json
    assunto = data.get('assunto')
    descricao = data.get('descricao')
    data_consulta = data.get('data')

    if not assunto or not descricao or not data_consulta:
        return jsonify({"erro": "Assunto, descrição e data são obrigatórios!"}), 400

    # Insere nova consulta
    consulta_input = {'assunto': assunto, 'descricao': descricao, 'data': data_consulta}
    consultas.insert_one(consulta_input)
    
    return jsonify({"mensagem": "Consulta cadastrada com sucesso!"}), 201

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

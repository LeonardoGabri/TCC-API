from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import psycopg2 as pg
import uuid
import configparser
import requests

controller = Flask(__name__)
CORS(controller)

config = configparser.ConfigParser()
config.read('application.properties')

connection = pg.connect(
        database = config.get('app','POSTGRES_DB_RAILWAY'),
        host = config.get('app','POSTGRES_HOST_RAILWAY'),
        user = config.get('app','POSTGRES_USERNAME_RAILWAY'),
        password = config.get('app','POSTGRES_PASSWORD_RAILWAY'),
        port = config.get('app','POSTGRES_PORT_RAILWAY')
    )

cursor = connection.cursor()

# @controller.route('/anemometro', methods=['GET'])
# def listar_registros_anemometro():
#     query = "SELECT * FROM anemometro"
#     df = pd.read_sql_query(query, con=connection)
#     registros = df.to_dict(orient='records')
#     return jsonify(registros)

@controller.route('/anemometro', methods=['GET'])
def listar_registros_anemometro():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    start_index = (page - 1) * per_page

    query = f"SELECT * FROM anemometro123 WHERE velocidade > 0 ORDER BY data DESC LIMIT {per_page} OFFSET {start_index}"
    df = pd.read_sql_query(query, con=connection)
    registros = df.to_dict(orient='records')

    return jsonify(registros)

@controller.route('/anemometro/<id>', methods=['GET'])
def obter_registro_anemometro_id(id):
    query = "SELECT * FROM anemometro123 as l where l.id = '" + id + "'"
    df = pd.read_sql_query(query, con=connection)
    return df.to_dict(orient='records')
        
@controller.route('/anemometro', methods=['POST'])
def incluir_registro_anemometro():
    uuidRandom = uuid.uuid4()
    query = "INSERT INTO anemometro (id, angulo, velocidade, direcao) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (
        str(uuidRandom),
        str(request.get_json().get('angulo')),
        str(request.get_json().get('velocidade')),
        str(request.get_json().get('direcao'))
    )
                   )
    connection.commit()
    return obter_registro_anemometro_id(str(uuidRandom))

@controller.route('/anemometro/<id>', methods=['DELETE'])
def delete_registro_anemometro(id):
    query = "DELETE FROM anemometro as l where l.id = '" + id + "'"
    cursor.execute(query, str(id))
    connection.commit()
    return "Excluído"

@controller.route('/portas/<funcionamento_normal>', methods=['GET'])
def inserir_comando_portas(funcionamento_normal):
    uuidRandom = str(uuid.uuid4())
    ultimo_registro = listar_registros_portas()

    print(str(ultimo_registro['funcionamento_normal']).lower())
    print(funcionamento_normal)
    if str(ultimo_registro['funcionamento_normal']).lower() == funcionamento_normal:
        return jsonify('O funcionamento já está configurado.')

    delete_registro_portas(ultimo_registro['id'])

    query = "INSERT INTO portas (id, funcionamento_normal) VALUES(%s, %s)"
    cursor.execute(query, (uuidRandom, funcionamento_normal))
    connection.commit()

    return jsonify('Comando para inserção de comando das portas executado com sucesso!')


@controller.route('/portas', methods=['GET'])
def listar_registros_portas():
    query = f"SELECT * FROM portas"
    df = pd.read_sql_query(query, con=connection)
    registros = df.to_dict(orient='records')

    return registros[0]

def delete_registro_portas(id):
    query = "DELETE FROM portas as l where l.id = '" + id + "'"
    cursor.execute(query, str(id))
    connection.commit()
    return "Excluído"


controller.run(port=5000, host='localhost', debug=True)



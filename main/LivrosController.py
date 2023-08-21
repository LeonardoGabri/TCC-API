from flask import Flask, request, jsonify
import pandas as pd
import psycopg2 as pg
import uuid
import configparser
from decimal import Decimal

controller = Flask(__name__)

config = configparser.ConfigParser()
config.read('application.properties')

connection = pg.connect(
        database = config.get('app','POSTGRES_DB'),
        host = config.get('app','POSTGRES_HOST'),
        user = config.get('app','POSTGRES_USERNAME'),
        password = config.get('app','POSTGRES_PASSWORD'),
        port = config.get('app','POSTGRES_PORT')
    )

# connection = pg.connect(
#         database = 'tcc',
#         host = 'localhost',
#         user = 'tcc',
#         password = 'tcc20202023',
#         port = '5432'
#     )

cursor = connection.cursor()

@controller.route('/registros-anemometro', methods=['GET'])
def listar_registros_anemometro():
    query = "SELECT * FROM anemometro"
    df = pd.read_sql_query(query, con=connection)
    registros = df.to_dict(orient='records')
    return jsonify(registros)

@controller.route('/registro-anemometro/<id>', methods=['GET'])
def obter_registro_anemometro_id(id):
    query = "SELECT * FROM anemometro as l where l.id = '" + id + "'"
    df = pd.read_sql_query(query, con=connection)
    return df.to_dict(orient='records')
        
@controller.route('/anemometro', methods=['POST'])
def incluir_registro_anemometro():
    uuidRandom = uuid.uuid4()
    query = "INSERT INTO anemometro (id, velocidade, direcao, energiageradacalculada) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (
        str(uuidRandom),
        Decimal(request.get_json().get('velocidade')),
        request.get_json().get('direcao'),
        Decimal(request.get_json().get('energiageradacalculada'))
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

# -------------------------------------------------------------------------
@controller.route('/registros-gerador', methods=['GET'])
def listar_registros_gerador():
    query = "SELECT * FROM minigerador"
    df = pd.read_sql_query(query, con=connection)
    registros = df.to_dict(orient='records')
    return jsonify(registros)


@controller.route('/registro-minigerador/<id>', methods=['GET'])
def obter_registro_anemometro_id(id):
    query = "SELECT * FROM minigerador as l where l.id = '" + id + "'"
    df = pd.read_sql_query(query, con=connection)
    return df.to_dict(orient='records')


@controller.route('/minigerador', methods=['POST'])
def incluir_registro_minigerador():
    uuidRandom = uuid.uuid4()
    query = "INSERT INTO minigerador (id, velocidade, portanorte, portasul, portaleste, portaoeste, energiagerada) VALUES(%s, %s, %s, %s, %s, %s, %s,)"
    cursor.execute(query, (
        str(uuidRandom),
        Decimal(request.get_json().get('velocidade')),
        Decimal(request.get_json().get('portanorte')),
        Decimal(request.get_json().get('portasul')),
        Decimal(request.get_json().get('portaleste')),
        Decimal(request.get_json().get('portaoeste')),
        Decimal(request.get_json().get('energiagerada')),
        ),
    )
    connection.commit()
    return obter_registro_anemometro_id(str(uuidRandom))

@controller.route('/minigerador/<id>', methods=['DELETE'])
def delete_registro_anemometro(id):
    query = "DELETE FROM minigerador as l where l.id = '" + id + "'"
    cursor.execute(query, str(id))
    connection.commit()
    return "Excluído"

controller.run(port=5000, host='localhost', debug=True)



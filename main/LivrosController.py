from flask import Flask, request, jsonify
import pandas as pd
import psycopg2 as pg
import uuid
import configparser

controller = Flask(__name__)

config = configparser.ConfigParser()
config.read('application.properties')

# connection = pg.connect(
#         database = config.get('app','POSTGRES_DB'),
#         host = config.get('app','POSTGRES_HOST'),
#         user = config.get('app','POSTGRES_USERNAME'),
#         password = config.get('app','POSTGRES_PASSWORD'),
#         port = config.get('app','POSTGRES_PORT')
#     )

connection = pg.connect(
        database = 'tcc',
        host = 'localhost',
        user = 'tcc',
        password = 'tcc20202023',
        port = '5432'
    )

cursor = connection.cursor()

@controller.route('/livros', methods=['GET'])
def obter_livros():
    query = "SELECT * FROM livros"
    df = pd.read_sql_query(query, con=connection)
    livros = df.to_dict(orient='records')
    return jsonify(livros)

@controller.route('/livro/<id>', methods=['GET'])
def obter_livro_id(id):
    query = "SELECT * FROM livros as l where l.id = '" + id + "'"
    df = pd.read_sql_query(query, con=connection)
    return df.to_dict(orient='records')
        
@controller.route('/livro', methods=['POST'])
def incluir_livro():
    uuidRandom = uuid.uuid4()
    query = "INSERT INTO livros (id, autor, titulo) VALUES(%s, %s, %s)"
    cursor.execute(query, (str(uuidRandom), request.get_json().get('autor'), request.get_json().get('titulo')))
    connection.commit()
    return obter_livro_id(str(uuidRandom))

@controller.route('/livro/<id>', methods=['DELETE'])
def delete_livro(id):
    print("TIPO", type(id))
    query = "DELETE FROM livros as l where l.id = '" + id + "'"
    cursor.execute(query, str(id))
    connection.commit()
    return "Excluído"

controller.run(port=5000, host='localhost', debug=True)



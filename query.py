import argparse
import json
from pymongo import MongoClient
import os
import pymongo

# Função para realizar find
def realizar_find(collection, query, limit=None, count=False):
    if count:
        total = collection.count_documents(query)
        print(f"Total de documentos: {total}")
    else:
        result = collection.find(query)
        if limit:
            result = result.limit(limit)
        for doc in result:
            print(doc)

# Função para realizar find all
def realizar_find_all(collection, limit=None, count=False):
    if count:
        total = collection.count_documents({})
        print(f"Total de documentos: {total}")
    else:
        result = collection.find({})
        if limit:
            result = result.limit(limit)
        for doc in result:
            print(doc)

# Função para realizar aggregate
def realizar_aggregate(collection, pipeline, limit=None, count=False):
    if count:
        result = list(collection.aggregate(pipeline))
        total = len(result)
        print(f"Total de documentos: {total}")
    else:
        if limit:
            pipeline.append({"$limit": limit})
        result = collection.aggregate(pipeline)
        for doc in result:
            print(doc)

# Função principal
def main():
    # Configuração do argumento da linha de comando
    parser = argparse.ArgumentParser(description='Script para realizar operações find, find_all ou aggregate no MongoDB.')
    parser.add_argument('operation', choices=['find', 'find_all', 'aggregate'], help='Tipo de operação a ser realizada.')
    parser.add_argument('query', type=str, nargs='?', default='{}', help='Consulta em formato JSON (não requerido para find_all).')
    parser.add_argument('database', type=str, help='Nome do banco de dados.')
    parser.add_argument('collection', type=str, help='Nome da coleção.')
    parser.add_argument('--limit', type=int, help='Número máximo de documentos a serem retornados.')
    parser.add_argument('--count', action='store_true', help='Retornar a contagem de documentos em vez dos documentos.')

    args = parser.parse_args()
    
    # Configurações da conexão MongoDB
    USERNAME = "teste"
    PASSWORD = "senha"
    CLUSTER_ENDPOINT = "documentdb-cluster.cluster-cnsm04002u0o.us-east-2.docdb.amazonaws.com"
    PORT = 27017
    cert = "cert/global-bundle.pem"

    # Verifica o caminho do certificado
    if not os.path.exists(cert):
        print(f"O arquivo de certificado não foi encontrado no caminho: {cert}")
        return

    uri = (f"mongodb://{USERNAME}:{PASSWORD}@{CLUSTER_ENDPOINT}:{PORT}/"
           f"?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false")

    client = MongoClient(uri,
                         tls=True,
                         tlsCAFile=cert,  # Caminho para o arquivo de certificado TLS
                         socketTimeoutMS=30000,
                         connectTimeoutMS=30000)
    try:
        # Conectando ao Amazon DocumentDB
        client.server_info()  # Testando a conexão
        print("Conexão estabelecida com sucesso!")

        db = client[args.database]
        collection = db[args.collection]

        query = json.loads(args.query)

        if args.operation == 'find':
            realizar_find(collection, query, args.limit, args.count)
        elif args.operation == 'find_all':
            realizar_find_all(collection, args.limit, args.count)
        elif args.operation == 'aggregate':
            realizar_aggregate(collection, query, args.limit, args.count)

    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Erro de timeout ao conectar ao Amazon DocumentDB:", err)
    except json.JSONDecodeError as json_err:
        print("Erro ao decodificar JSON:", json_err)
    finally:
        client.close()

if __name__ == '__main__':
    main()

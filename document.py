import string
from pymongo import MongoClient
import random
import os
import pymongo

DB_NAME = 'databaseTest'
COLLECTION1_NAME = 'collectionOne'
COLLECTION2_NAME = 'collectionTwo'
USERNAME = "teste"
PASSWORD = "senha"
CLUSTER_ENDPOINT = "documentdb-cluster.cluster-cnsm04002u0o.us-east-2.docdb.amazonaws.com"
PORT = 27017

# Função para gerar dados aleatórios
def gerar_dados_aleatorios(num_docs):
    dados = []
    for _ in range(num_docs):
        documento = {
            'nome': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            'idade': random.randint(18, 70),
            'cidade': ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
            'ativo': random.choice([True, False])
        }
        dados.append(documento)
    return dados

cert = "cert/global-bundle.pem"

# Verifica o caminho do certificado
try:
    if os.path.exists(cert):
        with open(cert, 'r') as f:
            content = f.read()
            print("Certificado lido com sucesso!")
    else:
        print(f"O arquivo de certificado não foi encontrado no caminho: {cert}")
except Exception as e:
    print(f"Erro ao tentar ler o certificado: {e}")

# Nome do conjunto de réplicas
replica_set_name = "rs0"

uri = (f"mongodb://{USERNAME}:{PASSWORD}@{CLUSTER_ENDPOINT}:{PORT}/"
       f"?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false")

client = MongoClient(uri,
                     tls=True,
                     tlsAllowInvalidCertificates=True,  # Se necessário, dependendo da sua configuração de certificação
                     socketTimeoutMS=30000,
                     connectTimeoutMS=30000)
try:
    # Conectando ao Amazon DocumentDB
    
    # Testando a conexão
    client.server_info()
    print("Conexão estabelecida com sucesso!")

    db = client[DB_NAME]

    # Criando as coleções
    collection1 = db[COLLECTION1_NAME]
    collection2 = db[COLLECTION2_NAME]

    # Inserindo dados aleatórios nas coleções
    dados_colecao1 = gerar_dados_aleatorios(10)
    dados_colecao2 = gerar_dados_aleatorios(10)

    collection1.insert_many(dados_colecao1)
    collection2.insert_many(dados_colecao2)

    print("Dados inseridos com sucesso!")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print("Erro de timeout ao conectar ao Amazon DocumentDB:", err)
finally:
    client.close()

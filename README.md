# DocumentDB
## Construção do Ambiente
Criação da EC2 com AMI Linux Ubuntu - GNU/Linux 6.8.0-1009-aws x86_64 - ubuntu@<ip>
Private key salva em cert/teste.pem + configuração de permissionamento do arquivo: chmod 600 cert/teste.pem
Acesso a EC2 via terminal: ssh -i cert/teste.pem ubuntu@<ip>

> System information as of Thu Aug  1 16:18:44 UTC 2024
> 
>   System load:  0.0               Processes:             106
>   Usage of /:   22.9% of 6.71GB   Users logged in:       1
>   Memory usage: 19%               IPv4 address for enX0: <ip>
>   Swap usage:   0%
> 
> 
> Expanded Security Maintenance for Applications is not enabled.
> 
> 0 updates can be applied immediately.

### Preparação do ambiente:
sudo apt update
sudo apt install python3 python3-pip -y

### Preparação dos arquivos:
mkdir -p ~/cert
cd ~/cert
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
cd ..
nano ~/script.py
<adicionar o conteúdo de document.py, criação do database, collections e ingestão de dados>

### Preparação do ambiente do Python:
sudo apt install python3-venv -y
python3 -m venv ~/myenv
source ~/myenv/bin/activate
pip install pymongo //para instalação do driver de MongoDB para Python
python ~/script.py

Logs:
Certificado lido com sucesso!
/home/ubuntu/script.py:47: UserWarning: You appear to be connected to a DocumentDB cluster. For more information regarding feature compatibility and support please visit https://www.mongodb.com/supportability/documentdb
  client = MongoClient(uri,
Conexão estabelecida com sucesso!
Dados inseridos com sucesso!

Dados:
{'_id': ObjectId('66abb7c516cc6c74a72ade8c'), 'nome': '3YS6U2UC3K', 'idade': 43, 'cidade': 'WKQ2K', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade8d'), 'nome': '5EUOVQ71VU', 'idade': 56, 'cidade': 'CBJP2', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade8e'), 'nome': 'JJODGQ010G', 'idade': 46, 'cidade': '2QWFT', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade8f'), 'nome': 'OEE2C3WABD', 'idade': 40, 'cidade': 'VG5YX', 'ativo': True}
{'_id': ObjectId('66abb7c516cc6c74a72ade90'), 'nome': 'KNIS2CUU4K', 'idade': 35, 'cidade': 'DIKRD', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade91'), 'nome': '7OLPA3KOTT', 'idade': 53, 'cidade': 'N0IX4', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade92'), 'nome': 'CWBT4OICXO', 'idade': 41, 'cidade': 'MAL1G', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade93'), 'nome': 'HEKDZXC6DT', 'idade': 46, 'cidade': 'X3RZI', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade94'), 'nome': 'ZBLR3NEF7B', 'idade': 18, 'cidade': 'O5N7S', 'ativo': True}
{'_id': ObjectId('66abb7c516cc6c74a72ade95'), 'nome': 'UCBGVXHX6N', 'idade': 35, 'cidade': '9U82A', 'ativo': False}


Comandos de Teste:
python3 ~/query.py find '{"idade": 46}' databaseTest collectionOne

{'_id': ObjectId('66abb7c516cc6c74a72ade8e'), 'nome': 'JJODGQ010G', 'idade': 46, 'cidade': '2QWFT', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade93'), 'nome': 'HEKDZXC6DT', 'idade': 46, 'cidade': 'X3RZI', 'ativo': False}


python3 mongo_query.py find_all databaseTest collectionOne

{'_id': ObjectId('66abb7c516cc6c74a72ade8c'), 'nome': '3YS6U2UC3K', 'idade': 43, 'cidade': 'WKQ2K', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade8d'), 'nome': '5EUOVQ71VU', 'idade': 56, 'cidade': 'CBJP2', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade8e'), 'nome': 'JJODGQ010G', 'idade': 46, 'cidade': '2QWFT', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade8f'), 'nome': 'OEE2C3WABD', 'idade': 40, 'cidade': 'VG5YX', 'ativo': True}
{'_id': ObjectId('66abb7c516cc6c74a72ade90'), 'nome': 'KNIS2CUU4K', 'idade': 35, 'cidade': 'DIKRD', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade91'), 'nome': '7OLPA3KOTT', 'idade': 53, 'cidade': 'N0IX4', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade92'), 'nome': 'CWBT4OICXO', 'idade': 41, 'cidade': 'MAL1G', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade93'), 'nome': 'HEKDZXC6DT', 'idade': 46, 'cidade': 'X3RZI', 'ativo': False}
{'_id': ObjectId('66abb7c516cc6c74a72ade94'), 'nome': 'ZBLR3NEF7B', 'idade': 18, 'cidade': 'O5N7S', 'ativo': True}
{'_id': ObjectId('66abb7c516cc6c74a72ade95'), 'nome': 'UCBGVXHX6N', 'idade': 35, 'cidade': '9U82A', 'ativo': False}


python3 ~/query.py aggregate '[{"$group": {"_id": "$cidade", "total": {"$sum": 1}}}]' databaseTest collectionOne

{'_id': '9U82A', 'total': 1}
{'_id': 'WKQ2K', 'total': 1}
{'_id': 'N0IX4', 'total': 1}
{'_id': '2QWFT', 'total': 1}
{'_id': 'MAL1G', 'total': 1}
{'_id': 'VG5YX', 'total': 1}
{'_id': 'CBJP2', 'total': 1}
{'_id': 'DIKRD', 'total': 1}
{'_id': 'O5N7S', 'total': 1}
{'_id': 'X3RZI', 'total': 1}


python3 ~/query.py find '{"idade": 46}' databaseTest collectionOne --limit 5 --count

Total de documentos: 2


python3 ~/query.py find_all databaseTest collectionOne --limit 10 --count

Total de documentos: 10


python3 ~/query.py aggregate '[{"$group": {"_id": "$cidade", "total": {"$sum": 1}}}]' databaseT
est collectionOne --limit 5 --count

Total de documentos: 10
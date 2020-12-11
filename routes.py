from flask import Flask, jsonify, request, json

app = Flask('Ebanx')
# EBANX Software Engineer Take-home assignment
# Icaro Quintao
# Versões: Python 3.7.4, Flask 1.1.2
# Utilizei o Postman para auxiliar nos testes locais

# Referências: 
# Question marks in Flask Urls for routing [duplicate]. Stackoverflow, 2017. Disponível em: <https://stackoverflow.com/questions/40658566/question-marks-in-flask-urls-for-routing>. Acesso em: 28/10/2020.
# WRIGHT, Jake. Building a REST API in Python. YouTube, 2018. Disponível em: <https://www.youtube.com/watch?v=4T5Gnrmzjak&t=674s&ab_channel=JakeWright>. Acesso em: 28/10/2020.

# A variável datas armazena todos as requisições recebidas pela API, depositos, transferências e retiradas.
datas = [    
    {
        'id': 1,
        'type': 'deposit',
        'destination': '100',
        'amount': '10'
    },
    {
        'id': 2,
        'type': 'deposit',
        'destination': '100',
        'amount': '10'
    },
        {
        'id': 3,
        'type': 'withdraw',
        'destination': '100',
        'amount': '10'
    }
]
# A variável operations armazena todas operações feitas pela API, no caso do depósito ela recebe uma destination, no caso de saque ela recebe origin e transferência ela recebe os dois.
operations = [    
    {"destination":{
        'id': "1",
        'balance': 20,
        
    }},
    {"destination":{
        'id': "2",
        'balance': 200,
    }},
    {"destination":{
        'id': "3",
        'balance': 50,
    }},
    {"origin": {
        "id":"50", 
        "balance":15
    }}
]
# A variável balances representa uma conta, com id e saldo.
balances = [    
    {
        'id': "1",
        'balance': 20,
        
    },
    {
        'id': "2",
        'balance': 200,
    },
    {
        'id': "3",
        'balance': 50,
    }
]
# variáveis com dados para testes, são apagados no /reset e não interferem no programa (:

# A função deposito recebe um json
def deposito(evento):
        # percorre todas as contas
        balanco = [balance['balance'] for balance in balances if balance['id'] == evento['destination']]
        # caso a conta não exista, cria
        if balanco == []:
            # cria a conta
            conta = {
                'id': evento['destination'],
                'balance': evento['amount']
            }
            # registra a operação
            operation = {}
            operation['destination'] = conta
            # salva os dados e retorna
            datas.append(evento)
            balances.append(conta)
            operations.append(operation)
            return jsonify(operation), 201
        # caso a conta já exista
        else:
            # percorre todas as contas
            for balance in balances:
                # onde a conta for a de destino
                if balance['id'] == evento['destination']:
                    # soma o valor que está na conta com o valor que se está recebendo
                    aux = int(balanco[0]) + evento['amount']
                    # registra o novo balanço da conta
                    balance['balance'] = aux
                    # registra a operação
                    operation = {"destination": {
                        'id': evento['destination'],
                        'balance': aux
                    }}
                    # salva os demais dados e retorna
                    operations.append(operation)
                    datas.append(evento)
                    return jsonify(operation), 201

# A função saque recebe um json
def saque(evento):
    # recebe, caso exista, o balanço da conta para saque  
    balanco = [balance['balance'] for balance in balances if balance['id'] == evento['origin']]
    # se não existir, retorna not found
    if balanco == []:
        return '0', 404
    # se existir
    else:
        # percorre as contas
        for balance in balances:
            # acha a conta para efetuar a retirada
            if balance['id'] == evento['origin']:
                # subtrai o valor do saque no balanço da conta (obs: não verifica se a pessoa possui o saldo ou n)
                aux = int(balanco[0]) - evento['amount']
                # armazena o novo balanço da conta
                balance['balance'] = aux
                # cria a operação
                operation = {"origin": 
                {"id": balance['id'], 
                "balance": aux
                }}
                # salva os demais dados e retorna
                datas.append(evento)
                operations.append(operation)
                return jsonify(operation), 201

# A função transfere recebe um json
# Tentei de todo jeito utilizar as funções saque e deposito aqui, porém como o retorno delas era no formato: (<Response 42 bytes [200 OK]>, 201) obs: no caso de created
# acabei optando por implementar a função separadamente
def transfere(evento):
    # pega o balanço da conta de origem
    balancoOrigem = [balance['balance'] for balance in balances if balance['id'] == evento['origin']]
    # caso essa conta não exita, retorna not found
    if balancoOrigem == []:
        return '0', 404
    # caso exista, podemos realizar a transferência
    else:
        # busca o balanço da conta de destino
        balancoDest = [balance['balance'] for balance in balances if balance['id'] == evento['destination']]
        # caso a conta de destino não exista, cria
        if balancoDest == []:
            conta = {
                'id': evento['destination'],
                'balance': 0
            }
            balances.append(conta)
        # percorre todas as cotnas
        for balance in balances:
            # acha a conta de origem
            if balance['id'] == evento['origin']:
                # subtrai o valor da transferência no balanço da conta de origem (obs: não verifica se a pessoa possui o saldo ou n)
                aux = int(balancoOrigem[0]) - evento['amount']
                # armazena o novo balanço
                balance['balance'] = aux
                # cria a parte da origem na operação
                origem = {"id": balance['id'], 
                "balance": aux
                }
            # acha a conta de destino
            if balance['id'] == evento['destination']:
                balancoDest = [balance['balance'] for balance in balances if balance['id'] == evento['destination']]
                # soma o balanço da conta com o valor que está sendo transferido
                aux2 = int(balancoDest[0]) + evento['amount']
                # atualiza o balanço da conta
                balance['balance'] = aux2
                # cria a parte do destino na operação
                destino = {"id": balance['id'], 
                "balance": aux2
                }
        # cria a operação
        operation = {}
        operation['origin'] = origem
        operation['destination'] = destino
        # salva os demais dados e retorna
        datas.append(evento)
        operations.append(operation)
        return jsonify(operation), 201

                    


# Rota de reset
# Apaga os dados das variáveis datas, operations e balances e retorna OK 200.
@app.route('/reset', methods=['POST'])
def reset():
    datas.clear()
    operations.clear()
    balances.clear()
    res = 'OK'
    status = 200
    return res, status

# Rota balance
@app.route('/balance', methods=['GET'])
def balance():
    # armazena o id. 
    id = request.args.get('account_id', None)
    # percorre as contas e acha o id que foi requisitado
    balanco = [balance['balance'] for balance in balances if balance['id'] == id]
    # caso o balanço não seja nulo
    if balanco != []:
        # retorna o balanço da conta
        return str(balanco[0]), 200
    # caso seja nulo, retorna not found
    return '0', 404
    
# Rota event
@app.route("/event", methods=['POST'])
def event():
    # converte a requisição em json
    evento = request.get_json()
    # dependendo do tipo, direciona para a função específica
    if evento['type'] == 'deposit':
        return deposito(evento)
    
    if evento['type'] == 'withdraw':
        return saque(evento)
    
    if evento['type'] == 'transfer':
        return transfere(evento)

# Rota relatório apenas para consultar as variáveis datas, operations e balances com o Postman
@app.route('/relatorio', methods=['GET'])
def relatorio():
    rel = {}
    rel['registros'] = datas
    rel['ops'] = operations
    rel['contas'] = balances
    return jsonify(rel), 201

app.run()
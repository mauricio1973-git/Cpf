import json

def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (ex: 111.111.111-11 não é válido)
    if cpf == cpf[0] * len(cpf):
        return False
    
    # Função para calcular o dígito verificador
    def calcular_digito(cpf, peso_inicial):
        soma = 0
        for i in range(peso_inicial):
            soma += int(cpf[i]) * (peso_inicial + 1 - i)
        digito = (soma * 10 % 11) % 10
        return digito
    
    # Calcula os dois dígitos verificadores
    digito_1 = calcular_digito(cpf, 9)
    digito_2 = calcular_digito(cpf, 10)
    
    # Verifica se os dígitos calculados são iguais aos dígitos do CPF
    return cpf[-2:] == f"{digito_1}{digito_2}"

def lambda_handler(event, context):
    # Extrai o CPF do corpo da requisição
    body = json.loads(event['body'])
    cpf = body.get('cpf', '')
    
    # Valida o CPF
    is_valid = validar_cpf(cpf)
    
    # Retorna a resposta
    return {
        'statusCode': 200,
        'body': json.dumps({
            'cpf': cpf,
            'valid': is_valid
        })
    }

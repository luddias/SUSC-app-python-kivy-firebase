#  -----------------------------------------------------------------------
#   .* APLICATIVO COM KIVY - PYTHON - FIREBASE *.
# 
#    database.py - Arquivo utilizado como módulo no main.py, possui funções 
#    auxiliares para acesso ao banco de dados(firebase) e realização de
#    algumas tarefas dentro do aplicativo.
# 
#    Copyright 2022 Ludmila Dias
# 
#   ----------------------------------------------------------------------

#   IMPORTAÇÃO DE BIBLIOTECAS
import json
import requests
import datetime

#   LINK DATABASE
link="https://susc-ludmiladias-default-rtdb.firebaseio.com/"

#   CADASTRAR NOVO USUARIO
def cadastro_usuario(nome,email,cpf,senha):
    cadastro={'cpf':cpf, 'email':email, 'nome': nome, 'senha' : senha}
    requisicao= requests.post(f'{link}/Funcionarios/.json', data=json.dumps(cadastro))
    return True

#   VERIFICAR SE CPF JÁ ESTA CADASTRADO
def verifica_cpf_cadastro(cpf):
    requisicao=requests.get(f'{link}/Funcionarios/.json')
    dic_requisicao=requisicao.json()
    for id_funcionario in dic_requisicao:
        cpfbd=dic_requisicao[id_funcionario]['cpf']
        if cpfbd==cpf:
            return False
    return True

#   VERIFICAR SE O PACIENTE ESTÁ CADASTRADO
def verifica_cpf_agendamento(cpf):
    requisicao=requests.get(f'{link}/Pacientes/.json')
    dic_requisicao=requisicao.json()
    for id_paciente in dic_requisicao:
        cpfbd=dic_requisicao[id_paciente]['cpf']
        if cpfbd==cpf:
            return True
        
    return False

#   VERIFICAR SE O CPF É VALIDO
def cpf_validate(numbers):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True

#   VERIFICAR SE O EMAIL JÁ ESTA CADASTRADO
def verifica_email_cadastro(email):
    requisicao=requests.get(f'{link}/Funcionarios/.json')
    dic_requisicao=requisicao.json()
    for id_funcionario in dic_requisicao:
        emailbd=dic_requisicao[id_funcionario]['email']
        if emailbd==email:
            return False
    return True

#   REDEFINIR SENHA
def redefinir_senha(email, senha):
    requisicao=requests.get(f'{link}/Funcionarios/.json')
    dic_requisicao=requisicao.json()
    for id_funcionario in dic_requisicao:
        emailbd=dic_requisicao[id_funcionario]['email']
        if emailbd==email:
            dado={'senha':senha}
            requisicao=requests.patch(f'{link}/Funcionarios/{id_funcionario}/.json', data=json.dumps(dado))
            return True
    return False

#   ALTERAR DADOS
def alterar_dados(id,nome, email, cpf, senha):
    requisicao=requests.get(f'{link}/Funcionarios/.json')
    dic_requisicao=requisicao.json()
    for id_funcionario in dic_requisicao:
        if id_funcionario==id:
            novasenha={'senha':senha}
            novocpf={'cpf':cpf}
            novonome={'nome':nome}
            novoemail={'email':email}
            requisicao=requests.patch(f'{link}/Funcionarios/{id_funcionario}/.json', data=json.dumps(novasenha))
            requisicao=requests.patch(f'{link}/Funcionarios/{id_funcionario}/.json', data=json.dumps(novocpf))
            requisicao=requests.patch(f'{link}/Funcionarios/{id_funcionario}/.json', data=json.dumps(novonome))
            requisicao=requests.patch(f'{link}/Funcionarios/{id_funcionario}/.json', data=json.dumps(novoemail))
            return True
    return False

#   AGENDAR UMA CONSULTA
def agendar_consulta(paciente,especialidade,data):
    id=(contalista("Consultas")+1)
    dados={'id': id, 'data':data, 'especialidade':especialidade, 'paciente':paciente}
    requisicao= requests.post(f'{link}/Consultas/.json', data=json.dumps(dados))
    return True

#   VERIFICAR MEDICAMENTO (QUANTIDADE)
def verifica_estoque(medicamento):
    requisicao=requests.get(f'{link}/Medicamentos/.json')
    dic_requisicao=requisicao.json()
    for id_medicamento in dic_requisicao:
        nomebd=dic_requisicao[id_medicamento]['nome']
        if nomebd==medicamento:
            if dic_requisicao[id_medicamento]['quantidade']>0:
                return True
            else:
                return False

#   VERIFICAR MEDICAMENTO (EXISTENCIA)
def verifica_medicamento(medicamento):
    requisicao=requests.get(f'{link}/Medicamentos/.json')
    dic_requisicao=requisicao.json()
    for id_medicamento in dic_requisicao:
        nomebd=dic_requisicao[id_medicamento]['nome']
        if nomebd==medicamento:
            return True
    return False

#   VERIFICAR DATA DE REMESSA MEDICAMENTO
def verifica_remessa(medicamento):
    requisicao=requests.get(f'{link}/Medicamentos/.json')
    dic_requisicao=requisicao.json()
    for id_medicamento in dic_requisicao:
        nomebd=dic_requisicao[id_medicamento]['nome']
        if nomebd==medicamento:
            data=dic_requisicao[id_medicamento]['prox_remessa']
            return data

#   VERIFICAR MEDICAMENTO (POR ID)
def verifica_meddado(id_dado):
    requisicao=requests.get(f'{link}/Medicamentos/.json')
    dic_requisicao=requisicao.json()
    for id_med in dic_requisicao:
        idbd=dic_requisicao[id_med]['id_medicamento']
        if int(idbd)==int(id_dado):
            return True
    return False

#   CONTADOR DE ITENS NA TABELA DO BANCO DE DADOS
def contalista(tipo):
    cont=0
    requisicao=requests.get(f'{link}/{tipo}/.json')
    dic_requisicao=requisicao.json()
    for id in dic_requisicao:
        cont+=1
    return cont

#   AGENDAR UMA RETIRADA
def agendar_retirada(paciente,medicamento,data):
    id=(contalista("Retiradas")+1)
    dados={'id':id,'data':data, 'medicamento':medicamento, 'paciente':paciente}
    requisicao= requests.post(f'{link}/Retiradas/.json', data=json.dumps(dados))
    return True

#   ACESSAR DADOS PARA TABELA PACIENTES
def dadosPacientes():
    lst=[]
    id=""
    requisicao=requests.get(f'{link}/Pacientes/.json')
    dic_requisicao=requisicao.json()
    for id_paciente in dic_requisicao:
        cpfbd=dic_requisicao[id_paciente]['cpf']
        nomebd=dic_requisicao[id_paciente]['nome']
        telefonebd=dic_requisicao[id_paciente]['telefone']
        paciente=(cpfbd, nomebd, telefonebd)
        lst.append(paciente)
    print(lst)
    return lst

#   ACESSAR DADOS PARA TABELA MEDICAMENTOS
def dadosMedicamentos():
    lst=[]
    requisicao=requests.get(f'{link}/Medicamentos/.json')
    dic_requisicao=requisicao.json()
    for id_remedio in dic_requisicao:
        idbd=dic_requisicao[id_remedio]['id_medicamento']
        nomebd=dic_requisicao[id_remedio]['nome']
        quantbd=dic_requisicao[id_remedio]['quantidade']
        databd=dic_requisicao[id_remedio]['prox_remessa']
        medicamento=(idbd, nomebd, quantbd, databd)
        lst.append(medicamento)
    print(lst)
    return lst

#   VERIFICAR DATA
def verificardata(data):
    datalista=data.split('/')
    current_time = datetime.datetime.now() 
    if int(datalista[2])>=current_time.year:
        if int(datalista[1])>=current_time.month:
            if int(datalista[0])>=current_time.day:
                return True
    return False        

#   ACESSAR DADOS PARA TABELA CONSULTAS E RETIRADAS
def dadosAgendamentos():
    lst=[]
    requisicao=requests.get(f'{link}/Consultas/.json')
    dic_requisicao=requisicao.json()
    for id in dic_requisicao:
        databd=dic_requisicao[id]['data']
        if verificardata(databd):
            cpfbd=dic_requisicao[id]['paciente']
            idbd=dic_requisicao[id]['id']
            consulta=(idbd, cpfbd, databd, "Consulta")
            lst.append(consulta)
    requisicao=requests.get(f'{link}/Retiradas/.json')
    dic_requisicao=requisicao.json()
    for id in dic_requisicao:
        databd=dic_requisicao[id]['data']
        if verificardata(databd):
            cpfbd=dic_requisicao[id]['paciente']
            idbd=dic_requisicao[id]['id']
            retirada=(idbd, cpfbd, databd, "Retirada")
            lst.append(retirada)
    print(lst)
    return lst
        
#   ATUALIZAR ESTOQUE
def atualizarEstoque(id, quant, operacao):
    requisicao=requests.get(f'{link}/Medicamentos/.json')
    dic_requisicao=requisicao.json()

    for id_med in dic_requisicao:
        idbd=dic_requisicao[id_med]['id_medicamento']
        if int(id)==int(idbd):
            quantbd=int(dic_requisicao[id_med]['quantidade'])
            if operacao=="s":
                dado={'quantidade':quantbd-int(quant)}
            elif operacao=="e":
                dado={'quantidade':quantbd+int(quant)}
            requisicao=requests.patch(f'{link}/Medicamentos/{id_med}/.json', data=json.dumps(dado))
    return True

#   ACESSAR NOME DO USUARIO
def id_dado_consulta():
    id=""
    requisicao=requests.get(f'{link}/Consultas/.json')
    dic_requisicao=requisicao.json()
    for id_consulta in dic_requisicao:
        paciente=dic_requisicao[id_consulta]['paciente']
        if paciente=='18223245600':
            id=id_consulta

#   VERIFICAR LOGIN
def verificar_login(cpf,senha):
    requisicao=requests.get(f'{link}/Funcionarios/.json')
    dic_requisicao=requisicao.json()
    for id_funcionario in dic_requisicao:
        cpfbd=dic_requisicao[id_funcionario]['cpf']
        senhabd=dic_requisicao[id_funcionario]['senha']
        if cpfbd==cpf:
            if senhabd==senha:
                return True
            else:
                return False
    return False

#   SALVAR DADOS USUARIO
def acessar_dados_usuario(cpf):
    requisicao=requests.get(f'{link}/Funcionarios/.json')
    dic_requisicao=requisicao.json()
    for id_funcionario in dic_requisicao:
        cpfbd=dic_requisicao[id_funcionario]['cpf']
        if cpfbd==cpf:
            emailbd=dic_requisicao[id_funcionario]['email']
            senhabd=dic_requisicao[id_funcionario]['senha']
            nomebd=dic_requisicao[id_funcionario]['nome']
            idbd=id_funcionario
            dados_usuario=[idbd, cpfbd, nomebd, emailbd, senhabd]
            return dados_usuario

#   DELETAR UMA CONSULTA
# requisicao=requests.delete(f'{link}/Consultas/{id}/.json')
# print(requisicao)


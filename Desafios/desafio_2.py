

def Depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito:\tR$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

usuarios = []
id = 0  

def cadastrar_usuario(usuarios):
    
    cpf = int(input("Informe o CPF do usuário (sem espaços): ").strip())
    usuario = filtra_usuario(cpf, usuarios)
    
    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return        
    
        
    nome = input("Informe o nome do usuário: ").strip()
    data_nascimento = input("Informe a data de nascimento do usuário (DD/MM/AAAA): ").strip()
    logradouro = input("Informe o logradouro do endereço: ").strip()
    numero = input("Informe o número do endereço: ").strip()
    bairro = input("Informe o bairro do endereço: ").strip()
    cidade = input("Informe a cidade do endereço (Cidade/UF): ").strip()

    
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}"

    global id 
    id += 1
    novo_usuario = {
        "id" : id,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }

    
    usuarios.append(novo_usuario)
    print("✅ Usuário cadastrado com sucesso!")

def filtra_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None
    
    
numero_conta = 0
contas = []
def cadastrar_conta(cpf):
    global numero_conta  # Pra poder modificar a variável de fora da função
    usuario = filtra_usuario(cpf, usuarios)
    if usuario:
        numero_conta += 1
        agencia = "0001"
        nova_conta = {
            "Usuário": usuario["nome"],  # Aqui é 'usuario', não 'usuarios'
            "Conta": numero_conta,
            "Agência": agencia
        }
        contas.append(nova_conta)
        print("✅ Conta cadastrada com sucesso!")
        return  # Encerra a função após cadastrar
    print("❌ Usuário não encontrado.")  # Só mostra isso se ninguém for encontrado
    

    
def Sacar(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque\tR$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def Extrato(saldo, /,  *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Cadastrar Usuário
[5] Mostrar usuário cadastrados
[6] Cadastrar conta
[7] Mostrar contas
[0] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
limite_saques = 3

while True:
    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = Depositar(saldo, valor, extrato)

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, numero_saques = saldo, extrato, numero_saques = Sacar(
    saldo=saldo,
    valor=valor,
    extrato=extrato,
    limite=limite,
    numero_saques=numero_saques,
    limite_saques=limite_saques
)


    elif opcao == "3":
        Extrato(saldo, extrato=extrato)
    
    elif opcao == "4":
        
        cadastrar_usuario(usuarios)
    
    elif opcao == "5":
        for usuario in usuarios:
            print(usuario)
    
    
    
    elif opcao == "6":
        cpf = int(input("Informe o CPF do usuário que quer cadastrar uma conta: "))
        cadastrar_conta(cpf)
    
    elif opcao == "7":
        for conta in contas:
            print(f"""\
Conta: {conta["Conta"]}
C/c: {conta["Agência"]}
Titular: {conta["Usuário"]}
{"=" * 100}
                """)
        
            
    elif opcao == "0":
        print("Obrigado por usar nosso sistema bancário. Até logo!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

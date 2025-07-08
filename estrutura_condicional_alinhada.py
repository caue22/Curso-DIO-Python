conta_normal = False
saldo = 2000
saque = int(input("Informe o valor do saque: "))
cheque_especial = 450
conta_universitaria = False

if conta_normal:
    if saldo >= saque:
        print("Saque realizado com sucesso!")
    elif saque <= (saldo + cheque_especial):
        print("Saque realizado com uso do cheque especial!")
    else:
        print("Saque não realizado, saldo insuficiente!")

if conta_universitaria:
    if saldo >= saque:
        print("Saldo realizado com sucesso!")
    else:
        print("Saldo Insuficiente!")
else:
     print("Sistema não reconheceu op tipo de conta")
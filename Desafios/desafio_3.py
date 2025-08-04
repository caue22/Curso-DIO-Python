from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

# Transações
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass
    
    @property
    def valor(self):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Histórico
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now()
        })
        
# Cliente
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
        
    @property
    def contas(self):
        return self._contas

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def realizar_transacao(self, conta, transacao):
            transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# Conta
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        cliente.adicionar_conta(self)

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero = numero, cliente = cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    
    def sacar(self, valor):
        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False
        if valor <= 0:
            print("Valor inválido.")
            return False
        self._saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido.")
            return False
        self._saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        return True


# Conta Corrente
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
                Agência: \t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
            """

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_clientes(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n🚩Cliente não possui conta🚩")
        return
    
     # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    
    if not cliente:
        print("\n🚩Cliente não encontrado!🚩")
        return
    
    valor = float(input("Informe o valor do deposito: R$"))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    
    if not cliente:
        print("\n🚩Cliente não encontrado!🚩")
        return
    
    valor = float(input("Informe o valor do saque: R$"))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    
    if not cliente:
        print("\n🚩Cliente não encontrado!🚩")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n===================== EXTRATO ====================")
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas transações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
            
    print(extrato)
    print(f"\nSaldo: \n\t{conta.saldo:.2f}")
    print("===================================================")
    
def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    
    if cliente:
        print("\n🚩Já existe cliente com esse CPF!🚩")
        return

    nome = input("Infrome o nome completo: ")
    data_nascimento = input("Informe a data de nascimen (DD/MM/AAAA): ")
    endereco = input("Informe o endereço (rua, nro - bairro - cidade/UF - cep): ")
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    
    print("\n✅Cliente criado com sucesso!✅")
    
def criar_contas(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    
    if not cliente:
        print("🚩Cliente não encontrado, fluxo de criação de conta encerrado!🚩")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    
    print("\n✅Conta criada com sucesso!✅")
          
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "d":
            depositar(clientes)
        
        elif opcao == "s":
            sacar(clientes)
            
        elif opcao == "e":
            exibir_extrato(clientes)
            
        elif opcao == "nu":
            criar_cliente(clientes)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_contas(numero_conta, clientes, contas)
            
        elif opcao== "lc":
            listar_contas(contas)
            
        elif opcao == "q":
            break
        
        else:
            print("\n🚩Operação inválida, por favor selecione novemente a opção🚩")
            
main()
maior_idade = 18

idade_especial = 17

idade = int(input("Qual a sua idade? "))

if idade >= maior_idade:
    print("Você pode tirar a CNH")
elif idade == idade_especial:
    print("Pode fazer as aulas teoricas")
else:
    print("Não pode tirar CNH")
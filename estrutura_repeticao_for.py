texto = input("Informe um texto: ")

VOGAIS = "AEIOU"

print("Voagais do seu texto: ")

for letra in texto:
    if letra.upper() in VOGAIS:
        print(letra, end=" ")

print()
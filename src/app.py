gastos = []


def adicionar(valor, descricao):
    if valor < 0:
        raise ValueError("Valor não pode ser negativo")
    gastos.append({"valor": valor, "descricao": descricao})


def listar():
    return gastos


def total():
    return sum(g["valor"] for g in gastos)


def remover(index):
    if index < 0 or index >= len(gastos):
        raise IndexError("Índice inválido")
    gastos.pop(index)


def menu():
    while True:
        print("\n1 - Adicionar gasto")
        print("2 - Listar gastos")
        print("3 - Ver total")
        print("4 - Remover gasto")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            valor = float(input("Valor: "))
            desc = input("Descrição: ")
            adicionar(valor, desc)

        elif opcao == "2":
            for i, g in enumerate(listar()):
                print(f"{i} - {g['descricao']} | R${g['valor']}")

        elif opcao == "3":
            print(f"Total: R${total()}")

        elif opcao == "4":
            i = int(input("Índice: "))
            remover(i)

        elif opcao == "0":
            break

        else:
            print("Opção inválida")


if __name__ == "__main__":
    menu()
import json
import os
import time

DB_FILE = "tarefas.json"

# ----------------------------- #
# Funções utilitárias
# ----------------------------- #

def limpar_terminal():
    """Limpa o terminal conforme o sistema operacional."""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux / macOS
        os.system('clear')


# ----------------------------- #
# Funções de manipulação de dados
# ----------------------------- #

def carregar_tarefas():
    """Carrega as tarefas do arquivo JSON."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo JSON."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)


# ----------------------------- #
# Operações CRUD
# ----------------------------- #

def criar_tarefa(titulo, descricao):
    """Cria uma nova tarefa."""
    tarefas = carregar_tarefas()
    nova_tarefa = {
        "id": len(tarefas) + 1,
        "titulo": titulo,
        "descricao": descricao,
        "status": "Pendente"
    }
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    print(f"\n✅ Tarefa '{titulo}' criada com sucesso!")

def listar_tarefas():
    """Lista todas as tarefas e permite ver detalhes individuais."""
    tarefas = carregar_tarefas()
    if not tarefas:
        print("\n⚠️ Nenhuma tarefa cadastrada ainda.")
        input("\nPressione ENTER para voltar ao menu...")
        return

    while True:
        limpar_terminal()
        print("=== Lista de Tarefas ===\n")
        for tarefa in tarefas:
            print(f"[{tarefa['id']}] {tarefa['titulo']} - {tarefa['status']}")
        print("\nDigite o número da tarefa para ver os detalhes, ou 0 para voltar.")
        try:
            escolha = int(input("\nEscolha: "))
            if escolha == 0:
                break
            tarefa = next((t for t in tarefas if t["id"] == escolha), None)
            if tarefa:
                limpar_terminal()
                print("=== Detalhes da Tarefa ===\n")
                print(f"📌 ID: {tarefa['id']}")
                print(f"📖 Título: {tarefa['titulo']}")
                print(f"📝 Descrição: {tarefa['descricao']}")
                print(f"📊 Status: {tarefa['status']}")
                input("\nPressione ENTER para voltar à lista...")
            else:
                print("❌ Tarefa não encontrada.")
                time.sleep(1)
        except ValueError:
            print("⚠️ Entrada inválida. Digite um número.")
            time.sleep(1)

def atualizar_tarefa(id_tarefa, novo_status):
    """Atualiza o status de uma tarefa específica."""
    tarefas = carregar_tarefas()
    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefa["status"] = novo_status
            salvar_tarefas(tarefas)
            print(f"\n✅ Tarefa '{tarefa['titulo']}' atualizada para '{novo_status}'.")
            return
    print("❌ Tarefa não encontrada.")

def excluir_tarefa(id_tarefa):
    """Exclui uma tarefa específica e reorganiza os IDs."""
    tarefas = carregar_tarefas()
    tarefa_encontrada = False

    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefas.remove(tarefa)
            tarefa_encontrada = True
            print(f"\n🗑️ Tarefa '{tarefa['titulo']}' excluída com sucesso!")
            break

    if not tarefa_encontrada:
        print("❌ Tarefa não encontrada.")
        return

    # Reorganiza os IDs
    for i, tarefa in enumerate(tarefas, start=1):
        tarefa["id"] = i

    salvar_tarefas(tarefas)
    time.sleep(1)

def marcar_todas_como_concluidas():
    """Marca todas as tarefas como concluídas."""
    tarefas = carregar_tarefas()
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return
    for tarefa in tarefas:
        tarefa["status"] = "Concluída"
    salvar_tarefas(tarefas)
    print("\n🏁 Todas as tarefas foram marcadas como concluídas!")

def excluir_todas_as_tarefas():
    """Exclui todas as tarefas com confirmação explícita."""
    tarefas = carregar_tarefas()
    if not tarefas:
        print("Nenhuma tarefa encontrada para excluir.")
        input("\nPressione ENTER para voltar ao menu...")
        return

    print("⚠️ Esta ação vai excluir TODAS as tarefas da lista!")
    confirmacao = input('Para confirmar, digite exatamente: "Eu desejo excluir todos os itens da lista"\n\nDigite aqui: ')

    if confirmacao.strip() == "Eu desejo excluir todos os itens da lista":
        salvar_tarefas([])  # lista vazia
        print("\n🧹 Todas as tarefas foram excluídas com sucesso!")
    else:
        print("\n❌ A exclusão total foi cancelada.")


# ----------------------------- #
# Menu principal
# ----------------------------- #

def menu():
    while True:
        limpar_terminal()
        print("=== Gerenciador de Tarefas ===")
        print("1. Criar tarefa")
        print("2. Listar tarefas")
        print("3. Atualizar tarefa")
        print("4. Excluir tarefa")
        print("5. Marcar todas como concluídas")
        print("6. Excluir todas as tarefas")
        print("7. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            limpar_terminal()
            titulo = input("Título da tarefa: ")
            descricao = input("Descrição: ")
            criar_tarefa(titulo, descricao)
            input("\nPressione ENTER para voltar ao menu...")

        elif opcao == "2":
            listar_tarefas()

        elif opcao == "3":
            limpar_terminal()
            print("=== Atualizar Tarefa ===\n")

            tarefas = carregar_tarefas()
            if not tarefas:
                print("Nenhuma tarefa encontrada para atualizar.")
                input("\nPressione ENTER para voltar ao menu...")
                continue

            print("Tarefas atuais:\n")
            for tarefa in tarefas:
                print(f"[{tarefa['id']}] {tarefa['titulo']} - {tarefa['status']}")

            print("\n-------------------------------")
            try:
                id_tarefa = int(input("Digite o ID da tarefa que deseja atualizar: "))

                print("\nEscolha o novo status da tarefa:")
                print("1 - Pendente")
                print("2 - Em Progresso")
                print("3 - Concluída")

                opcao_status = input("Digite o número correspondente: ")

                if opcao_status == "1":
                    novo_status = "Pendente"
                elif opcao_status == "2":
                    novo_status = "Em Progresso"
                elif opcao_status == "3":
                    novo_status = "Concluída"
                else:
                    print("⚠️ Opção inválida. Status não alterado.")
                    input("\nPressione ENTER para voltar ao menu...")
                    continue

                atualizar_tarefa(id_tarefa, novo_status)

            except ValueError:
                print("⚠️ ID inválido. Digite um número.")

            input("\nPressione ENTER para voltar ao menu...")

        elif opcao == "4":
            limpar_terminal()
            print("=== Excluir Tarefa ===\n")

            tarefas = carregar_tarefas()
            if not tarefas:
                print("Nenhuma tarefa encontrada para excluir.")
                input("\nPressione ENTER para voltar ao menu...")
                continue

            print("Tarefas atuais:\n")
            for tarefa in tarefas:
                print(f"[{tarefa['id']}] {tarefa['titulo']} - {tarefa['status']}")

            print("\n-------------------------------")
            try:
                id_tarefa = int(input("Digite o ID da tarefa que deseja excluir: "))
                confirmacao = input(f"Tem certeza que deseja excluir a tarefa {id_tarefa}? (s/n): ").lower()
                if confirmacao == 's':
                    excluir_tarefa(id_tarefa)
                else:
                    print("Exclusão cancelada.")
            except ValueError:
                print("⚠️ ID inválido. Digite um número.")

            input("\nPressione ENTER para voltar ao menu...")

        elif opcao == "5":
            limpar_terminal()
            marcar_todas_como_concluidas()
            input("\nPressione ENTER para voltar ao menu...")

        elif opcao == "6":
            limpar_terminal()
            excluir_todas_as_tarefas()
            input("\nPressione ENTER para voltar ao menu...")

        elif opcao == "7":
            limpar_terminal()
            print("Saindo... 👋")
            break

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para tentar novamente...")


# ----------------------------- #
# Execução
# ----------------------------- #
if __name__ == "__main__":
    menu()

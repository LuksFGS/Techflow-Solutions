import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import main as app

def test_criar_tarefa(tmp_path):
    """Testa se uma tarefa é criada corretamente."""
    db_file = tmp_path / "tarefas.json"
    app.DB_FILE = str(db_file)

    app.criar_tarefa("Estudar", "Revisar conteúdo de Engenharia de Software")
    tarefas = app.carregar_tarefas()

    assert len(tarefas) == 1
    assert tarefas[0]["titulo"] == "Estudar"
    assert tarefas[0]["descricao"] == "Revisar conteúdo de Engenharia de Software"
    assert tarefas[0]["status"] == "Pendente"

def test_marcar_todas_como_concluidas(tmp_path):
    """Testa se todas as tarefas são marcadas como concluídas."""
    db_file = tmp_path / "tarefas.json"
    app.DB_FILE = str(db_file)

    app.criar_tarefa("Teste 1", "Descrição 1")
    app.criar_tarefa("Teste 2", "Descrição 2")

    app.marcar_todas_como_concluidas()
    tarefas = app.carregar_tarefas()

    assert all(t["status"] == "Concluída" for t in tarefas)

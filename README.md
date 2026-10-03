# Extração de palestrantes - Integra IF Goiano 2026

Projeto da disciplina de Linguagens Formais e Autômatos (Eng. de Computação - IF Goiano, Câmpus Trindade).

Automação em Python que baixa a página de eventos, extrai com **expressões regulares**
imagem, nome, local de trabalho e contato dos palestrantes, baixa as fotos e grava tudo em SQLite.

## Execução
    python main.py            # baixa a página e executa todas as tarefas
    python main.py --offline  # usa o pagina.txt existente, sem baixar o HTML
    python verificar.py       # confere banco, imagens e contagem

Requer apenas a biblioteca padrão do Python 3.9+.

## Arquivos
| Tarefa | Arquivo |
|---|---|
| 002 | tarefa002_baixar_html.py (gera pagina.txt) |
| 003 | tarefa003_extrair_dados.py |
| 004 | tarefa004_baixar_imagens.py (pasta download/) |
| 005 | tarefa005_criar_banco.py (event.db, tabela speaker) |
| 006 | tarefa006_registrar_dados.py |
| - | main.py (executa tudo), verificar.py (checagem) |

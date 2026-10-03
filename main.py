"""Executa todas as tarefas em sequência (002 a 006).

Uso:
    python main.py            # baixa a página da internet e faz tudo
    python main.py --offline  # usa o pagina.txt que já existe (sem baixar o HTML)
"""
import sys

from tarefa002_baixar_html import baixar_html
from tarefa003_extrair_dados import extrair_palestrantes
from tarefa004_baixar_imagens import baixar_imagens
from tarefa006_registrar_dados import registrar

if __name__ == "__main__":
    if "--offline" not in sys.argv:
        baixar_html()                          # tarefa 002
    palestrantes = extrair_palestrantes()      # tarefa 003
    baixar_imagens(palestrantes)               # tarefa 004
    registrar(palestrantes)                    # tarefas 005 e 006
    print("\nPronto! Rode 'python verificar.py' para conferir o resultado.")

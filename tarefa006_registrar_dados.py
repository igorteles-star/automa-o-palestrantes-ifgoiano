"""Tarefa 006 - Registra todos os dados dos palestrantes na tabela speaker."""
import sqlite3

from tarefa003_extrair_dados import extrair_palestrantes
from tarefa004_baixar_imagens import nome_do_arquivo
from tarefa005_criar_banco import BANCO, criar_banco


def registrar(palestrantes: list[dict]) -> None:
    criar_banco()
    con = sqlite3.connect(BANCO)
    with con:
        con.execute("DELETE FROM speaker")  # evita duplicar ao reexecutar
        con.execute("DELETE FROM sqlite_sequence WHERE name = 'speaker'")
        con.executemany(
            "INSERT INTO speaker (name, work, email, image) VALUES (?, ?, ?, ?)",
            [
                (p["name"], p["work"], p["email"], nome_do_arquivo(p["image_src"]))
                for p in palestrantes
            ],
        )
    con.close()
    print(f"[006] {len(palestrantes)} palestrantes registrados em '{BANCO}'")


if __name__ == "__main__":
    registrar(extrair_palestrantes())

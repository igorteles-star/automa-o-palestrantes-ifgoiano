"""Confere se o resultado está correto (banco, imagens e contagem)."""
import os
import re
import sqlite3

BANCO = "event.db"
PASTA = "download"
ARQUIVO_HTML = "pagina.txt"

ok = True


def checar(condicao: bool, mensagem: str) -> None:
    global ok
    print(("[OK]   " if condicao else "[ERRO] ") + mensagem)
    ok = ok and condicao


if not os.path.exists(BANCO):
    raise SystemExit("event.db não encontrado. Rode 'python main.py' primeiro.")

con = sqlite3.connect(BANCO)
linhas = con.execute("SELECT id, name, work, email, image FROM speaker").fetchall()
con.close()

# 1) contagem no banco x contagem no HTML
if os.path.exists(ARQUIVO_HTML):
    with open(ARQUIVO_HTML, encoding="utf-8") as f:
        esperado = len(re.findall(r'id="Palestrante\d+"', f.read()))
    checar(len(linhas) == esperado,
           f"banco tem {len(linhas)} registros; a página tem {esperado} palestrantes")
else:
    print(f"[AVISO] {ARQUIVO_HTML} não existe; contagem não comparada")

# 2) campos vazios
vazios = [l for l in linhas if not all(str(c).strip() for c in l[1:])]
checar(not vazios, "nenhum campo vazio na tabela" if not vazios
       else f"{len(vazios)} registro(s) com campo vazio: {[v[1] for v in vazios]}")

# 3) e-mails com formato válido
padrao = re.compile(r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$")
ruins = [l[1] for l in linhas if not padrao.match(l[3])]
checar(not ruins, "todos os e-mails têm formato válido" if not ruins
       else f"e-mail inválido em: {ruins}")

# 4) imagens existem na pasta download
faltam = [l[4] for l in linhas if not os.path.isfile(os.path.join(PASTA, l[4]))]
checar(not faltam, "todas as imagens do banco existem em download/" if not faltam
       else f"imagens ausentes em download/: {faltam}")

print("\nTudo certo!" if ok else "\nHá problemas acima.")
print("\nRegistros:")
for l in linhas:
    print(f"  {l[0]:>2} | {l[1]} | {l[3]} | {l[4]}")

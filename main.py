"""
Automação de processo: extração de palestrantes do portal de eventos do IF Goiano.

Tarefas cobertas (ver enunciado):
  002 - baixar o código-fonte da página e salvar em arquivo TXT
  003 - extrair imagem, nome, local de trabalho e contato com Expressões Regulares
  004 - baixar as imagens para a pasta "download"
  005 - criar o banco event.db com a tabela speaker
  006 - registrar os palestrantes na tabela speaker

Uso:  python main.py
"""
import html
import os
import re
import sqlite3
from urllib.parse import unquote, urljoin, urlparse

import requests

URL = "https://eventos.ifgoiano.edu.br/integra2026/"
ARQUIVO_TXT = "pagina.txt"
PASTA_DOWNLOAD = "download"
BANCO = "event.db"
HEADERS = {"User-Agent": "Mozilla/5.0 (trabalho-academico-LFA)"}

# ----------------------------------------------------------------------------
# Expressões regulares (flags: DOTALL para o "." atravessar quebras de linha)
# ----------------------------------------------------------------------------
# Bloco do card: id="PalestranteN" ... primeira <img ... src="..."> antes do próximo card.
# O trecho (?:(?!id="Palestrante\d+").)*? impede que a busca "invada" o card seguinte.
RE_CARD = re.compile(
    r'id="Palestrante(?P<n>\d+)"(?:(?!id="Palestrante\d+").)*?'
    r'<img[^>]*?\bsrc="(?P<src>[^"]+)"',
    re.DOTALL,
)

# Bloco do modal: começa em id="modalN" e vai até o próximo modal (ou fim do arquivo).
RE_MODAL = re.compile(
    r'id="modal(?P<n>\d+)"(?P<corpo>.*?)(?=id="modal\d+"|\Z)',
    re.DOTALL,
)

RE_NOME = re.compile(r"<h4[^>]*>(.*?)</h4>", re.DOTALL)       # nome completo
RE_LOCAL = re.compile(r"<h6[^>]*>(.*?)</h6>", re.DOTALL)      # local de trabalho
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")        # contato
RE_TAGS = re.compile(r"<[^>]+>")


def limpar(texto: str) -> str:
    """Remove tags internas, converte entidades HTML (&amp; etc.) e normaliza espaços."""
    texto = html.unescape(RE_TAGS.sub("", texto))
    return re.sub(r"\s+", " ", texto).strip()


# ----------------------------------------------------------------------------
# Tarefa 002
# ----------------------------------------------------------------------------
def baixar_codigo_fonte() -> str:
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    with open(ARQUIVO_TXT, "w", encoding="utf-8") as f:
        f.write(resp.text)
    print(f"[002] Código-fonte salvo em {ARQUIVO_TXT} ({len(resp.text)} caracteres)")
    return resp.text


# ----------------------------------------------------------------------------
# Tarefa 003
# ----------------------------------------------------------------------------
def extrair_palestrantes(conteudo: str) -> list[dict]:
    imagens = {m["n"]: m["src"] for m in RE_CARD.finditer(conteudo)}
    palestrantes = []

    for m in RE_MODAL.finditer(conteudo):
        n, corpo = m["n"], m["corpo"]
        nome = RE_NOME.search(corpo)
        local = RE_LOCAL.search(corpo)
        email = RE_EMAIL.search(corpo)
        src = imagens.get(n)

        if not nome:
            continue  # modal que não é de palestrante
        if not email:
            print(f"[003] Aviso: palestrante {n} ({limpar(nome.group(1))}) sem e-mail")

        palestrantes.append({
            "name": limpar(nome.group(1)),
            "work": limpar(local.group(1)) if local else "",
            "email": email.group(0) if email else "",
            "image_url": src,
            "image": os.path.basename(unquote(urlparse(src).path)) if src else "",
        })

    print(f"[003] {len(palestrantes)} palestrantes extraídos")
    return palestrantes


# ----------------------------------------------------------------------------
# Tarefa 004
# ----------------------------------------------------------------------------
def baixar_imagens(palestrantes: list[dict]) -> None:
    os.makedirs(PASTA_DOWNLOAD, exist_ok=True)
    for p in palestrantes:
        if not p["image_url"]:
            print(f"[004] {p['name']}: sem imagem")
            continue
        url = urljoin(URL, p["image_url"])  # src é relativo (/media/static/...)
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        with open(os.path.join(PASTA_DOWNLOAD, p["image"]), "wb") as f:
            f.write(resp.content)
        print(f"[004] {p['image']}")


# ----------------------------------------------------------------------------
# Tarefas 005 e 006
# ----------------------------------------------------------------------------
def criar_banco() -> sqlite3.Connection:
    conn = sqlite3.connect(BANCO)
    conn.execute("DROP TABLE IF EXISTS speaker")  # permite rodar o script várias vezes
    conn.execute(
        """
        CREATE TABLE speaker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            work VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            image VARCHAR(255) NOT NULL
        )
        """
    )
    conn.commit()
    print(f"[005] Banco {BANCO} criado com a tabela speaker")
    return conn


def registrar(conn: sqlite3.Connection, palestrantes: list[dict]) -> None:
    conn.executemany(
        "INSERT INTO speaker (name, work, email, image) VALUES (?, ?, ?, ?)",
        [(p["name"], p["work"], p["email"], p["image"]) for p in palestrantes],
    )
    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM speaker").fetchone()[0]
    print(f"[006] {total} registros na tabela speaker")


def main() -> None:
    conteudo = baixar_codigo_fonte()
    # Tarefa 003 lê do arquivo TXT gerado na 002, como pede o enunciado
    with open(ARQUIVO_TXT, encoding="utf-8") as f:
        conteudo = f.read()
    palestrantes = extrair_palestrantes(conteudo)
    baixar_imagens(palestrantes)
    conn = criar_banco()
    registrar(conn, palestrantes)
    conn.close()


if __name__ == "__main__":
    main()

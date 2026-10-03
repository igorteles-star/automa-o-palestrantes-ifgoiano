"""Tarefa 004 - Baixa as imagens dos palestrantes para a pasta 'download'."""
import os
import urllib.request
from urllib.parse import unquote, urljoin, urlparse

from tarefa002_baixar_html import URL
from tarefa003_extrair_dados import extrair_palestrantes

PASTA = "download"


def nome_do_arquivo(src: str) -> str:
    """'/media/static/palestrantes/Bia_YVs6RP1.png' -> 'Bia_YVs6RP1.png'"""
    return os.path.basename(unquote(urlparse(src).path))


def baixar_imagens(palestrantes: list[dict], base_url: str = URL) -> None:
    os.makedirs(PASTA, exist_ok=True)
    for p in palestrantes:
        if not p["image_src"]:
            print(f"[004] sem imagem: {p['name']}")
            continue
        arquivo = nome_do_arquivo(p["image_src"])
        destino = os.path.join(PASTA, arquivo)
        url = urljoin(base_url, p["image_src"])
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp, open(destino, "wb") as f:
                f.write(resp.read())
            print(f"[004] baixada: {arquivo}")
        except Exception as e:
            print(f"[004] ERRO em {url}: {e}")


if __name__ == "__main__":
    baixar_imagens(extrair_palestrantes())

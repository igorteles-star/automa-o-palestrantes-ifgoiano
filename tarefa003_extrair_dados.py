"""Tarefa 003 - Extrai com Expressões Regulares os dados de cada palestrante
a partir do arquivo TXT gerado na tarefa 002.

Estrutura do código-fonte (repete para cada palestrante):

  <div class="col-12 col-lg-3 gy-3 palestrante-item" id="Palestrante1" ...>
      ... <img src="/media/static/palestrantes/Bia_YVs6RP1.png" ...>        -> imagem
  </div>
  <div class="modal fade" id="modal1">
      ... <h4>Nome completo</h4> <br> <h6>Local de trabalho</h6> ...        -> nome / trabalho
      <div class="modal-body">
          <p>biografia ...</p>
          <p>email@dominio</p>                                              -> contato
          <p><a href="lattes...">...</a></p>                                (opcional)
      </div>
  </div>
"""
import html as htmllib
import re
import sys

ARQUIVO_ENTRADA = "pagina.txt"

# ---------------------------------------------------------------- blocos
# Bloco de cada card: grupo 1 = número, grupo 2 = conteúdo do card.
REGEX_BLOCO_CARD = re.compile(
    r'<div[^>]*palestrante-item[^>]*id="Palestrante(\d+)"'
    r'(.*?)(?=<div[^>]*class="modal fade"|\Z)',
    re.DOTALL,
)

# Bloco de cada modal: grupo 1 = número, grupo 2 = conteúdo do modal.
REGEX_BLOCO_MODAL = re.compile(
    r'<div[^>]*class="modal fade"[^>]*id="modal(\d+)"'
    r'(.*?)(?=<div[^>]*class="modal fade"|<div[^>]*palestrante-item|\Z)',
    re.DOTALL,
)

# ------------------------------------------------------- campos do palestrante
REGEX_IMAGEM = re.compile(r'<img[^>]*?src="([^"]+)"', re.DOTALL)
REGEX_NOME = re.compile(r"<h4[^>]*>(.*?)</h4>", re.DOTALL)
REGEX_TRABALHO = re.compile(r"<h6[^>]*>(.*?)</h6>", re.DOTALL)
# O contato é o <p> cujo conteúdo inteiro é um e-mail (a biografia e o link do
# Lattes também são <p>, mas não casam com este padrão).
REGEX_EMAIL = re.compile(
    r"<p[^>]*>\s*([\w.+-]+@[\w-]+(?:\.[\w-]+)+)\s*</p>", re.DOTALL
)

# ------------------------------------------------------------------ limpeza
REGEX_TAGS = re.compile(r"<[^>]+>")
REGEX_ESPACOS = re.compile(r"\s+")


def _limpar(texto: str) -> str:
    texto = REGEX_TAGS.sub("", texto)
    texto = htmllib.unescape(texto)
    return REGEX_ESPACOS.sub(" ", texto).strip()


def _primeiro(regex: re.Pattern, texto: str) -> str:
    m = regex.search(texto)
    return _limpar(m.group(1)) if m else ""


def extrair_palestrantes(caminho: str = ARQUIVO_ENTRADA) -> list[dict]:
    with open(caminho, encoding="utf-8") as f:
        conteudo = f.read()

    imagens = {n: _primeiro(REGEX_IMAGEM, bloco)
               for n, bloco in REGEX_BLOCO_CARD.findall(conteudo)}

    palestrantes = []
    for n, bloco in REGEX_BLOCO_MODAL.findall(conteudo):
        p = {
            "numero": int(n),
            "name": _primeiro(REGEX_NOME, bloco),
            "work": _primeiro(REGEX_TRABALHO, bloco),
            "email": _primeiro(REGEX_EMAIL, bloco),
            "image_src": imagens.get(n, ""),
        }
        faltando = [c for c in ("name", "work", "email", "image_src") if not p[c]]
        if faltando:
            print(f"[003] AVISO: palestrante {n} sem {', '.join(faltando)}")
        palestrantes.append(p)

    print(f"[003] {len(palestrantes)} palestrantes extraídos")
    return palestrantes


if __name__ == "__main__":
    arquivo = sys.argv[1] if len(sys.argv) > 1 else ARQUIVO_ENTRADA
    for p in extrair_palestrantes(arquivo):
        print(p)

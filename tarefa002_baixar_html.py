"""Tarefa 002 - Baixa o código-fonte da página e salva em um arquivo TXT."""
import urllib.request

URL = "https://eventos.ifgoiano.edu.br/integra2026/"
ARQUIVO_SAIDA = "pagina.txt"


def baixar_html(url: str = URL, saida: str = ARQUIVO_SAIDA) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        html = resp.read().decode(charset, errors="replace")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[002] Código-fonte salvo em '{saida}' ({len(html)} caracteres)")
    return html


if __name__ == "__main__":
    baixar_html()

"""Registro explícito das entradas e exportação rastreável de cada execução."""

from datetime import datetime, timezone
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
import platform
import subprocess
from uuid import uuid4

from .arquivos import RAIZ_PROJETO, calcular_sha256
from .visualizacoes import plotar_contabilidade_co2


def _json(valor):
    return json.dumps(valor, ensure_ascii=False, sort_keys=True, indent=2)


def _fontes(raiz, notebook):
    """Ignora outputs e contadores do notebook na identificação do código."""
    caminhos = sorted(set(
        list((raiz / "scr").glob("*.py"))
        + list((raiz / "scripts").glob("*.py"))
        + list((raiz / "parameters").rglob("SHA256SUMS"))
        + [raiz / "requirements.txt", raiz / "raw/SHA256SUMS",
           raiz / "references/sanguinet_azzoni_2024/SHA256SUMS",
           raiz / "parameters/exterior_representativo/README.md", notebook]
    ))
    resultado = {}
    for caminho in caminhos:
        texto = caminho.read_text(encoding="utf-8")
        if caminho == notebook:
            texto = _json([
                {"tipo": c["cell_type"], "fonte": "".join(c["source"])}
                for c in json.loads(texto)["cells"]
            ])
        resultado[caminho.relative_to(raiz).as_posix()] = {
            "sha256": sha256(texto.encode("utf-8")).hexdigest().upper(),
            "conteudo": texto,
        }
    return resultado


def _git(raiz):
    def executar(*args):
        return subprocess.check_output(
            ["git", "-C", str(raiz), *args], encoding="utf-8", stderr=subprocess.PIPE
        ).strip()
    try:
        commit = executar("rev-parse", "HEAD")
        estado = executar("status", "--porcelain", "--untracked-files=all")
        return {"commit": commit, "alteracoes_locais": bool(estado), "status": estado}
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "alteracoes_locais": None, "status": "Git indisponível"}


class Execucao:
    """Uma instância por execução completa do notebook, em kernel novo.

    A versão do notebook corresponde às células salvas em disco. O registro
    não captura edições não salvas nem alterações manuais de variáveis no kernel.
    """

    def __init__(self, notebook, *, raiz=RAIZ_PROJETO):
        self.raiz = Path(raiz).resolve()
        self.notebook = (self.raiz / notebook).resolve()
        self.entradas = []
        self._caminhos = {}
        self.registro = {
            "versao_manifesto": 1,
            "execucao_id": uuid4().hex,
            "inicio_utc": datetime.now(timezone.utc).isoformat(),
            "repositorio": _git(self.raiz),
            "notebook": self.notebook.relative_to(self.raiz).as_posix(),
            "fontes": _fontes(self.raiz, self.notebook),
            "ambiente": {
                "python": platform.python_version(),
                "plataforma": platform.platform(),
                "pacotes": {p: version(p) for p in
                            ("numpy", "pandas", "matplotlib", "seaborn", "xlrd")},
            },
            "entradas": self.entradas,
        }

    def carregar(self, leitor, caminho, descricao):
        """Registra apenas leituras concluídas, com os bytes estáveis na leitura."""
        caminho = Path(caminho).resolve()
        hash_antes = calcular_sha256(caminho)
        dados = leitor(caminho)  # O leitor verifica o manifesto esperado.
        if calcular_sha256(caminho) != hash_antes:
            raise ValueError(f"Arquivo alterado durante a leitura: {caminho}")
        nome = caminho.relative_to(self.raiz).as_posix() if caminho.is_relative_to(self.raiz) else str(caminho)
        entrada = {"arquivo": nome, "descricao": descricao, "sha256": hash_antes}
        if nome in self._caminhos:
            anterior = next(e for e in self.entradas if e["arquivo"] == nome)
            if anterior != entrada:
                raise ValueError("Entrada mudou nesta execução; reinicie a análise.")
        else:
            self.entradas.append(entrada)
            self._caminhos[nome] = caminho
        return dados

    def exportar(self, tabela, pasta, *, nome="contabilidade_co2_2018", titulo="Contabilidade setorial de CO2"):
        """Salva CSV, PNG com metadados e manifesto, em uma pasta exclusiva."""
        if not self.entradas:
            raise ValueError("Nenhuma entrada foi registrada nesta execução.")
        if Path(nome).name != nome:
            raise ValueError("O nome do output deve ser um nome simples de arquivo.")
        if _fontes(self.raiz, self.notebook) != self.registro["fontes"]:
            raise ValueError("Código ou notebook mudou durante a execução; execute novamente.")
        for entrada in self.entradas:
            if calcular_sha256(self._caminhos[entrada["arquivo"]]) != entrada["sha256"]:
                raise ValueError("Uma entrada mudou após a leitura; execute novamente.")
        destino = Path(pasta) / self.registro["execucao_id"]
        destino.mkdir(parents=True, exist_ok=False)
        csv = destino / f"{nome}.csv"
        png = destino / f"{nome}.png"
        manifesto = destino / f"{nome}.proveniencia.json"
        resumo = {k: v for k, v in self.registro.items() if k != "fontes"}
        resumo["notebook_sha256"] = self.registro["fontes"][self.registro["notebook"]]["sha256"]
        resumo["manifesto"] = manifesto.name
        tabela.to_csv(csv, encoding="utf-8", lineterminator="\n")
        figura, eixo = plotar_contabilidade_co2(
            tabela, png, titulo=titulo, metadados={"Proveniencia": _json(resumo)}
        )
        registro = {
            **self.registro,
            "fim_utc": datetime.now(timezone.utc).isoformat(),
            "outputs": [{"arquivo": p.name, "sha256": calcular_sha256(p)} for p in (csv, png)],
        }
        manifesto.write_text(_json(registro) + "\n", encoding="utf-8")
        return figura, eixo, manifesto

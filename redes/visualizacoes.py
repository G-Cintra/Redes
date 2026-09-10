"""Visualizações reutilizáveis do projeto."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plotar_contabilidade_co2(
    resultados: pd.DataFrame,
    caminho_saida: Path | str,
    *,
    titulo: str = "Contabilidade setorial de CO2",
    metadados: dict[str, str] | None = None,
) -> tuple[plt.Figure, plt.Axes]:
    """Gera e salva barras de consumo/renda e linha de producao por atividade.

    ``resultados`` deve ter uma atividade por linha e as colunas ``producao``,
    ``consumo`` e ``renda``. A coluna opcional ``descricao_atividade`` e usada
    nos rotulos do eixo vertical. O PNG e salvo em ``caminho_saida``.
    """
    colunas_necessarias = {"producao", "consumo", "renda"}
    colunas_ausentes = colunas_necessarias - set(resultados.columns)
    if colunas_ausentes:
        raise ValueError(f"Colunas ausentes para o grafico: {sorted(colunas_ausentes)}")
    if resultados.empty:
        raise ValueError("Nao e possivel gerar um grafico sem atividades.")

    dados = resultados.copy()
    dados.index = dados.index.astype(str)
    if "descricao_atividade" in dados:
        dados["atividade"] = dados.index + " - " + dados["descricao_atividade"].astype(str)
    else:
        dados["atividade"] = dados.index
    dados = dados.sort_values("producao", ascending=False)
    ordem = dados["atividade"].tolist()

    dados_barras = dados.melt(
        id_vars="atividade",
        value_vars=["consumo", "renda"],
        var_name="abordagem",
        value_name="emissoes_gg_co2",
    )

    altura = max(12, len(dados) * 0.38)
    figura, eixo = plt.subplots(figsize=(16, altura))
    sns.barplot(
        data=dados_barras,
        y="atividade",
        x="emissoes_gg_co2",
        hue="abordagem",
        hue_order=["consumo", "renda"],
        order=ordem,
        palette={"consumo": "#4C78A8", "renda": "#F58518"},
        errorbar=None,
        orient="h",
        ax=eixo,
    )
    sns.lineplot(
        data=dados,
        y="atividade",
        x="producao",
        sort=False,
        marker="o",
        markersize=4,
        linewidth=1.2,
        color="#202020",
        label="producao",
        estimator=None,
        errorbar=None,
        ax=eixo,
    )

    eixo.set_title(titulo)
    eixo.set_xlabel("Emissoes de CO2 (Gg)")
    eixo.set_ylabel("Atividade")
    eixo.legend(title="Abordagem", loc="lower right")
    figura.tight_layout()

    destino = Path(caminho_saida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=300, bbox_inches="tight", metadata=metadados)
    return figura, eixo

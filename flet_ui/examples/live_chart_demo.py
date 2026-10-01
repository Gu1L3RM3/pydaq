"""Exemplo Flet responsivo: um gráfico genérico e controles de demonstração.

Dependências:
    pip install "flet[all]" flet-charts
"""

import math
import random

import flet as ft
import flet_charts as fch


def main(page: ft.Page):
    page.title = "Painel de sinais"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 16
    page.bgcolor = ft.Colors.BLUE_GREY_50

    # Estado simples da série exibida. Troque estes valores pelos dados do seu sensor.
    valores = [4.0, 5.2, 4.6, 6.8, 6.1, 7.5, 7.0, 8.4]
    em_execucao = False

    status = ft.Text("Aguardando coleta", color=ft.Colors.BLUE_GREY_700)
    valor_atual = ft.Text(size=30, weight=ft.FontWeight.BOLD)

    serie = fch.LineChartData(
        color=ft.Colors.BLUE_600,
        stroke_width=3,
        curved=True,
        point=True,
    )

    grafico = fch.LineChart(
        data_series=[serie],
        min_x=0,
        max_x=7,
        min_y=0,
        max_y=10,
        interactive=True,
        expand=True,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
        border_radius=12,
        horizontal_grid_lines=fch.ChartGridLines(
            interval=2, color=ft.Colors.BLUE_GREY_100
        ),
    )

    def atualizar_grafico():
        """Atualiza pontos, escala e indicadores depois de alterar ``valores``."""
        serie.points = [
            fch.LineChartDataPoint(indice, valor)
            for indice, valor in enumerate(valores)
        ]
        grafico.max_x = max(1, len(valores) - 1)
        grafico.max_y = max(10, math.ceil(max(valores) + 1))
        valor_atual.value = f"{valores[-1]:.1f}"
        page.update()

    def iniciar_ou_pausar(e):
        nonlocal em_execucao
        em_execucao = not em_execucao
        e.control.text = "Pausar" if em_execucao else "Iniciar"
        e.control.icon = ft.Icons.PAUSE if em_execucao else ft.Icons.PLAY_ARROW
        status.value = "Coleta em execução" if em_execucao else "Coleta pausada"
        page.update()

    def adicionar_amostra(e):
        # Simula a chegada de uma amostra; substitua pela leitura do seu dispositivo.
        proximo = max(0, valores[-1] + random.uniform(-1.2, 1.2))
        valores.append(round(proximo, 2))
        if len(valores) > 20:
            valores.pop(0)
        status.value = "Nova amostra recebida"
        atualizar_grafico()

    def limpar(e):
        valores[:] = [0.0]
        status.value = "Série limpa"
        atualizar_grafico()

    botao_iniciar = ft.Button(
        "Iniciar", icon=ft.Icons.PLAY_ARROW, on_click=iniciar_ou_pausar
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Text("Monitor genérico", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("Exemplo responsivo para desktop e Android."),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                col={"xs": 12, "md": 4},
                                padding=16,
                                border_radius=12,
                                bgcolor=ft.Colors.WHITE,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Última leitura"),
                                        valor_atual,
                                        status,
                                    ]
                                ),
                            ),
                            ft.Container(
                                col={"xs": 12, "md": 8},
                                height=330,
                                content=grafico,
                            ),
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(col={"xs": 12, "sm": 4}, content=botao_iniciar),
                            ft.Container(
                                col={"xs": 12, "sm": 4},
                                content=ft.OutlinedButton(
                                    "Nova amostra", icon=ft.Icons.ADD, on_click=adicionar_amostra
                                ),
                            ),
                            ft.Container(
                                col={"xs": 12, "sm": 4},
                                content=ft.TextButton(
                                    "Limpar", icon=ft.Icons.DELETE_OUTLINE, on_click=limpar
                                ),
                            ),
                        ]
                    ),
                ],
            )
        )
    )
    atualizar_grafico()


if __name__ == "__main__":
    ft.run(main)

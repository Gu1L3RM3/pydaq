# Interface Flet do PYDAQ

Esta pasta contém a interface do PYDAQ em desenvolvimento com
[Flet](https://flet.dev/). Ela é independente da interface desktop atual,
baseada em PySide6, e por enquanto apresenta a estrutura visual e a navegação
das áreas do aplicativo.

## Pré-requisitos

- Python 3.10 a 3.12;
- dependências do projeto instaladas na raiz do repositório com `uv sync`, ou
  um ambiente virtual com `pip install -e .`.

Os comandos a seguir partem da raiz do repositório. Quando usar `pip` em vez
de `uv`, substitua `uv run flet` por `flet` (ou `python -m flet`).

## Executar no desktop

```console
cd flet_ui
uv run flet run -r main.py
```

O parâmetro `-r` observa alterações em `flet_ui/` e recarrega a aplicação.
Os recursos estáticos, como o logotipo, são lidos de `flet_ui/assets/`.

## Executar no Android com o aplicativo Flet

1. No celular Android, ative as **Opções do desenvolvedor** e a
   **Depuração USB**.
2. Conecte-o ao computador por USB e aceite a chave de depuração exibida no
   aparelho.
3. Verifique se o Flet encontra o dispositivo:

   ```console
   cd flet_ui
   uv run flet devices
   ```

4. Inicie a interface no celular:

   ```console
   uv run flet run --android main.py
   ```

O comando usa o fluxo de desenvolvimento do Flet e abre a aplicação no
telefone conectado. Para escolher um dispositivo específico quando houver mais
de um, use o ID exibido por `uv run flet devices` com os comandos de depuração
do Flet.

## Gerar e instalar um APK

Para criar um pacote Android instalável:

```console
cd flet_ui
uv run flet build apk .
```

O APK é salvo em `flet_ui/build/apk/`. Instale-o no dispositivo por ADB ou
copie o arquivo para o celular e permita a instalação de apps provenientes do
gerenciador de arquivos usado. Na primeira compilação, o Flet pode solicitar
ou baixar componentes do Flutter/Android necessários para o build.

## Arquivos principais

| Caminho | Finalidade |
| --- | --- |
| `main.py` | Ponto de entrada e composição da tela principal. |
| `theme.py` | Cores e tema compartilhados. |
| `components/` | Controles reutilizáveis (`navigation/`, formulários, gráfico). |
| `pages/` | Uma tela por rota; quando uma feature precisa de mais de um arquivo, vira `pages/<feature>/`. |
| `services/` | Ponte entre a UI e `pydaq.core`: leitura do formulário e sessão de aquisição em thread. |
| `assets/` | Imagens e outros recursos estáticos. |
| `examples/live_chart_demo.py` | Exemplo isolado de gráfico responsivo com Flet Charts. |
| `tests/` | Testes sem hardware; `tests/services/` espelha `services/`. |

A UI não importa nada de `pydaq.legacy_qt`. Ela usa `pydaq.core` (configuração,
lotes de amostras, protocolo `AcquisitionSource`) e os adaptadores em
`pydaq.devices`. Hoje a tela Get Data usa `pydaq.devices.simulated.SimulatedSource`.

Para executar o exemplo de gráfico:

```console
uv run --with flet-charts flet run examples/live_chart_demo.py
```

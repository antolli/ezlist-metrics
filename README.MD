# Gerador de Métricas de Usabilidade

Este módulo calcula métricas clássicas de usabilidade a partir de um arquivo CSV contendo dados de interação de usuários com um sistema.

## Instalação

Instale as dependências com:

```bash
pip install -r requirements.txt
```

## Como usar

Execute o módulo via linha de comando:

```bash
python -m gerar_metricas.main --csv caminho/para/dados.csv
```

> O CSV deve conter colunas como `Residente`, `Tarefa`, `Evento`, `Duração`, `Timestamp Final`, entre outras.

##  Métricas Disponíveis

### 1. Taxa de Conclusão de Tarefas (Completion Rate)
Proporção de tarefas concluídas com sucesso (evento “Sucesso”).

### 2. Tempo Médio
Tempo médio de execução por tarefa e por residente.

### 3. Taxa de Erros
Proporção de tarefas com eventos do tipo “problema de compreensão” ou “erro do usuário”.

### 4. Taxa de Aprendizado
Ganho de desempenho entre as Tarefas 1+2 e Tarefa 6 (de estrutura semelhante).

### 5. Eficiência Baseada no Tempo (TBE)
Métrica que considera a razão entre tarefas concluídas com sucesso e tempo total de execução.

## Estrutura

- `metrics/`: Funções para cálculo de cada métrica
- `main.py`: Ponto de entrada para geração das métricas

## Exemplo de Execução

```bash
python -m gerar_metricas.main --csv dados_usuarios.csv
```

As métricas serão exibidas diretamente no terminal.

# Gerador de Gráficos

Este módulo permite converter arquivos Excel para CSV e gerar dois tipos de gráficos baseados em dados de usabilidade de sistemas:  
- Gráfico de duração por evento e residente  
- Gráfico de frequência de tipos de eventos

## Instalação

Instale as dependências necessárias com:

```bash
pip install -r requirements.txt
```

## Como usar

Você pode executar o script `main.py` com diferentes argumentos:

### 1. Converter um arquivo Excel para CSV

```bash
python -m gerar_graficos.main --excel caminho/do/arquivo.xlsx --csv caminho/salvar.csv
```

### 2. Gerar gráfico de duração por evento e residente

```bash
python -m gerar_graficos.main --csv caminho/dados.csv --grafico duration
```

### 3. Gerar gráfico de barras com frequência de eventos

```bash
python -m gerar_graficos.main --csv caminho/dados.csv --grafico barras
```

> O parâmetro `--csv` é obrigatório para gerar gráficos.

## Estrutura

- `converter.py`: Função para converter Excel (.xlsx) em CSV (.csv)
- `plotting.py`: Funções de plotagem com matplotlib e plotly
- `main.py`: Script de linha de comando

## Requisitos

- pandas  
- matplotlib  
- plotly  
- openpyxl
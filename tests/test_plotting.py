import pandas as pd
import matplotlib.pyplot as plt
from gerar_graficos.plotting import plot_timeline, plot_event_frequency

def test_plot_duration(monkeypatch):
    # Garante que não há figuras abertas antes do teste
    plt.close('all')
    
    # Cria um DataFrame de exemplo com as colunas necessárias
    data = {
        'usuario': ['A', 'A', 'B', 'B'],
        'tempo': [1, 2, 1, 3],
        'tarefa': ['T1', 'T2', 'T1', 'T3'],
        'evento': ['inicio', 'problema', 'inicio', 'fim']
    }
    df = pd.DataFrame(data)
    
    # Suprime o plt.show para evitar que a janela do gráfico seja aberta durante o teste
    monkeypatch.setattr(plt, "show", lambda: None)
    
    # Chama a função de plotagem
    plot_duration(df)
    
    # Verifica se a figura foi criada: plt.get_fignums() retorna uma lista com os números das figuras ativas
    fig_nums = plt.get_fignums()
    assert len(fig_nums) > 0, "Nenhuma figura foi criada pela função plot_timeline."


def test_plot_event_frequency(monkeypatch):
    plt.close('all')
    
    data = {
        'evento': ['inicio', 'problema', 'inicio', 'fim', 'problema']
    }
    df = pd.DataFrame(data)
    
    monkeypatch.setattr(plt, "show", lambda: None)
    
    plot_event_frequency(df)
    
    fig_nums = plt.get_fignums()
    assert len(fig_nums) > 0, "Nenhuma figura foi criada pela função plot_event_frequency."
    
    
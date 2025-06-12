import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def plot_duration_with_means(df):
    """
    Plota um gráfico de barras empilhadas interativo com Plotly e,
    em seguida, calcula e imprime a média de duração por tipo de evento.
    """
    df = df.copy()

    # Filtra apenas eventos "não sucesso"
    df = df[~df['Evento'].str.lower().eq('sucesso')]

    # Converte "Duração" (HH:MM:SS) em segundos
    df['Duração'] = pd.to_timedelta(df['Duração'], errors='coerce').dt.total_seconds()
    df = df.dropna(subset=['Duração'])
    df['Duração'] = df['Duração'].round(0).astype(int)

    # --- Gráfico empilhado ---
    df_grouped = df.groupby(['Residente', 'Evento'], as_index=False)['Duração'].sum()
    fig = px.bar(
        df_grouped,
        x='Residente',
        y='Duração',
        color='Evento',
        hover_data={'Evento': True, 'Duração': ':.1f'},
        labels={'Duração': 'Duração (segundos)'},
        title='Duração total por Residente e Evento',
        category_orders={'Residente': [f'P{str(i).zfill(2)}' for i in range(1,11)]}
    )
    fig.update_layout(barmode='stack', xaxis_title="Residente", yaxis_title="Duração (segundos)")
    fig.show()

    # --- Cálculo das médias ---
    df_means = (
        df
        .groupby('Evento')['Duração']
        .mean()
        .reset_index(name='Média_segundos')
    )
    # opcional: adicionar coluna em minutos
    df_means['Média_minutos'] = (df_means['Média_segundos'] / 60).round(2)

    print("\nMédia de duração por evento:")
    print(df_means.to_string(index=False))

    return df_means

def plot_duration(df):
    """
    Plota um gráfico de barras empilhadas interativo com Plotly.
    Cada residente terá uma barra empilhada por evento e, ao passar o mouse,
    serão exibidos os detalhes (nome do evento e duração, em minutos).
    """
    df = df.copy()

    df = df[~df['Evento'].str.lower().eq('sucesso')]

    # Coluna "Duração" no formato "HH:MM:SS", converte para segundos.
    df['Duração'] = pd.to_timedelta(df['Duração'], errors='coerce').dt.total_seconds()
    df = df.dropna(subset=['Duração'])
    
    # Arredonda para int
    df['Duração'] = df['Duração'].round(0).astype(int)
    
    df_grouped = df.groupby(['Residente', 'Evento'], as_index=False)['Duração'].sum()
    
    fig = px.bar(
        df_grouped,
        x='Residente',
        y='Duração',
        color='Evento',
        text=None,
        hover_data={'Evento': True, 'Duração': ':.1f'}, 
        labels={'Duração': 'Duração (segundos)'},
        title='Duração total por Residente e Evento',
        category_orders={
        'Residente': ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10']
    }
    )
    
    fig.update_layout(barmode='stack', xaxis_title="Residente", yaxis_title="Duração (minutos)")
    
    fig.show()


def plot_event_frequency(df: pd.DataFrame) -> None:
    """
    Plota um gráfico de barras mostrando a frequência dos tipos de eventos.
    Eixo x: tipos de evento; Eixo y: frequência.
    """
    df.columns = df.columns.str.strip()
    
    if 'Evento' not in df.columns:
        print("Coluna 'Evento' não encontrada no CSV.")
        return
    
    df = df[~df['Evento'].str.lower().eq('sucesso')]
    
    freq = df['Evento'].value_counts()
    
    plt.figure(figsize=(10, 6))
    plt.bar(freq.index, freq.values)
    plt.xlabel("Tipo de Evento")
    plt.ylabel("Frequência")
    plt.title("Frequência de Tipos de Problemas")
    plt.show()

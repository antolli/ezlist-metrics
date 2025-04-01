import pandas as pd

def calculate_completion_rate(df: pd.DataFrame) -> float:
    """
    Calcula a Taxa de Conclusão de Tarefas (Completion Rate) a partir de um DataFrame
    que contenha as colunas: 'Residente', 'Tarefa' e 'Evento'.
    
    Retorna um valor em percentual (0 a 100).
    """
    df.columns = df.columns.str.strip()

    required_cols = ['Residente', 'Tarefa', 'Evento']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Coluna '{col}' não encontrada no DataFrame.")

    # Agrupa por (Residente, Tarefa) e verifica se existe algum 'Evento' == 'sucesso'
    # O resultado será um Series booleana, onde True significa que houve "sucesso" naquela tarefa
    tarefas_com_sucesso = df.groupby(['Residente', 'Tarefa'])['Evento'] \
                            .apply(lambda eventos: eventos.str.lower().eq('sucesso').any())

    total_tarefas = get_total_tarefas(df)
    tarefas_sucesso = tarefas_com_sucesso.sum() 
    
    if total_tarefas == 0:
        efetividade = 0.0
    else:
        efetividade = (tarefas_sucesso / total_tarefas) * 100

    per_resident = tarefas_com_sucesso.groupby('Residente').mean() * 100

    return efetividade, per_resident

def calculate_average_time(df: pd.DataFrame):
    """
    Calcula o tempo médio (em segundos) de execução das tarefas.
    - Tempo médio geral (para todas as tarefas)
    - Tempo médio por Residente
    - Tempo médio por Tarefa

    Retorna:
      - average_time_overall: float
      - average_time_by_resident: Series (index=Residente, values=tempo médio)
      - average_time_by_task: Series (index=Tarefa, values=tempo médio)
    """
    df.columns = df.columns.str.strip()

    required_cols = ['Residente', 'Tarefa', 'Duração']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Coluna '{col}' não encontrada no DataFrame.")

    if df['Duração'].dtype == object:
        df['Duração'] = pd.to_timedelta(df['Duração'], errors='coerce').dt.total_seconds()
        df = df.dropna(subset=['Duração']) 

    total_tarefas = get_total_tarefas(df)
    total_tempo = df['Duração'].sum()
    average_time_overall = (total_tempo / total_tarefas) if total_tarefas > 0 else 0.0

    # Tempo médio por Residente
    # 1) Agrupa por Residente
    # 2) Calcula média da coluna "Duração"
    average_time_by_resident = df.groupby('Residente')['Duração'].mean()

    # Tempo médio por Tarefa
    average_time_by_task = df.groupby('Tarefa')['Duração'].mean()

    return average_time_overall, average_time_by_resident, average_time_by_task


def get_total_tarefas(df: pd.DataFrame):

    df['Tarefa'] = df['Tarefa'].astype(str).str.strip().str.lower()

    df.columns = df.columns.str.strip()
    
    if 'Residente' not in df.columns or 'Tarefa' not in df.columns:
        raise ValueError("As colunas 'Residente' e 'Tarefa' são necessárias.")
    
    unique_tasks_by_resident = df.groupby('Residente')['Tarefa'].nunique()
    total_unique_tasks = unique_tasks_by_resident.sum()

    return total_unique_tasks
    
def calculate_error_rate(df: pd.DataFrame):
    """
    Calcula a Taxa de Erros considerando que:
      - Os eventos considerados como erro são: "problema de compreensao" e "erro do usuario".
      - Cada linha (interação) referente a uma tarefa é considerada.
      
    Retorna:
      - overall_error_rate: Taxa global de erro (em %), ou seja,
           (número total de interações de erro) / (total de interações) * 100.
      - error_rate_by_resident: Series com a taxa de erro por Residente (em %).
    """
    df = df.copy()
    
    df.columns = df.columns.str.strip()
    df['Evento'] = df['Evento'].astype(str).str.strip().str.lower()
    
    error_events = ['problema de compreensao', 'erro do usuario']
    
    df['is_error'] = df['Evento'].isin(error_events)
    
    total_interactions = len(df)
    total_errors = df['is_error'].sum()
    
    overall_error_rate = (total_errors / total_interactions * 100) if total_interactions > 0 else 0.0
    
    # Calcula a taxa de erro por Residente: para cada residente, é a média dos valores booleanos (True=1)
    error_rate_by_resident = df.groupby('Residente')['is_error'].mean() * 100
    
    return overall_error_rate, error_rate_by_resident

def calculate_total_time_for_task(df: pd.DataFrame, task: str) -> pd.Series:
    """
    Para cada residente, calcula o tempo total da tarefa como a diferença entre 00:00:00
    e o maior valor de 'Timestamp Final' para aquela tarefa.
    
    Parâmetros:
      - df: DataFrame com as colunas 'Residente', 'Tarefa' e 'Timestamp Final'
      - task: Nome da tarefa (ex: "Tarefa 1"). A comparação é feita ignorando espaços e case.
    
    Retorna:
      Uma Series com índice 'Residente' e o tempo total (em segundos) para a tarefa.
    """
    df['Tarefa'] = df['Tarefa'].astype(str).str.strip().str.lower()
    task = task.strip().lower()
    
    df_task = df[df['Tarefa'] == task].copy()
    
    df_task['Timestamp Final'] = pd.to_timedelta(df_task['Timestamp Final'], errors='coerce')
    df_task = df_task.dropna(subset=['Timestamp Final'])
    
    total_time = df_task.groupby('Residente')['Timestamp Final'].max()
    
    total_time_seconds = total_time.dt.total_seconds()
    
    return total_time_seconds

def calculate_learning_rate(df: pd.DataFrame):
    """
    Calcula a Taxa de Aprendizagem para cada residente, usando o tempo total de cada tarefa
    (calculado a partir do maior 'Timestamp Final').
    
    Fórmula: ((Tempo Tarefa Inicial - Tempo Tarefa Final) / Tempo Tarefa Inicial) * 100
    
    Retorna:
      - learning_rate_by_resident: Series com a taxa de aprendizagem (em %) por residente.
      - overall_learning_rate: Média das taxas de aprendizagem dos residentes.
    """
    time_initial = (calculate_total_time_for_task(df, 'Tarefa 1') + calculate_total_time_for_task(df, 'Tarefa 2'))
    print(time_initial)
    time_final   = calculate_total_time_for_task(df, 'Tarefa 6')
    print(time_final)
    df_times = pd.concat([time_initial, time_final], axis=1)
    df_times.columns = ['initial_time', 'final_time']
    
    df_times['learning_rate'] = df_times.apply(
        lambda row: ((row['initial_time'] - row['final_time']) / row['initial_time'] * 100)
                    if row['initial_time'] > 0 else 0.0,
        axis=1
    )
    
    return df_times['learning_rate'], df_times['learning_rate'].mean()

def calculate_completion_rate(df: pd.DataFrame):
    """
    Calcula a Eficiência Baseada no Tempo (Time-Based Efficiency) usando a fórmula:
    
      TBE = (1/(R*N)) * sum_{i=1..R, j=1..N} ( n_ij / t_ij )
    
    onde:
      - n_ij = 1 se a tarefa j do residente i foi concluída com sucesso; 0 caso contrário
      - t_ij = tempo (em segundos) até o último Timestamp Final da tarefa j do residente i
      - R = número de residentes (únicos) no dataset
      - N = número de tarefas (únicas) no dataset
    """
    df.columns = df.columns.str.strip()
    df['Residente'] = df['Residente'].astype(str).str.strip().str.lower()
    df['Tarefa'] = df['Tarefa'].astype(str).str.strip().str.lower()
    df['Evento'] = df['Evento'].astype(str).str.strip().str.lower()

    df['Timestamp Final'] = pd.to_timedelta(df['Timestamp Final'], errors='coerce')
    df = df.dropna(subset=['Timestamp Final'])
    
    # Agrupa por (Residente, Tarefa) para:
    #   - Pegar o último timestamp (maior)
    #   - Verificar se houve 'sucesso'
    grouped = df.groupby(['Residente', 'Tarefa']).agg(
        max_time=('Timestamp Final', 'max'),
        success_flag=('Evento', lambda ev: (ev == 'sucesso').any())
    ).reset_index()
    
    grouped['t_ij'] = grouped['max_time'].dt.total_seconds()

    grouped['n_ij'] = grouped['success_flag'].astype(int)
    
    # Agora calculamos n_ij / t_ij para cada par
    # (se t_ij = 0, definimos ratio = 0 para evitar divisão por zero)
    def ratio_calc(row):
        if row['t_ij'] > 0:
            return row['n_ij'] / row['t_ij']
        else:
            return 0.0

    grouped['ratio_ij'] = grouped.apply(ratio_calc, axis=1)


    R = grouped['Residente'].nunique()
    N = grouped['Tarefa'].nunique()
    

    sum_ratios = grouped['ratio_ij'].sum()
    if R == 0 or N == 0:
        return 0.0

    tbe = (1 / (R * N)) * sum_ratios
    
    # --- Impressões de depuração  ---
    print("\n=== Debug / Valores Intermediários ===")
    print("R (número de residentes):", R)
    print("N (número de tarefas):", N)
    print("\n--- Detalhes por (Residente, Tarefa) ---")
    print(grouped[['Residente', 'Tarefa', 'n_ij', 't_ij', 'ratio_ij']])
    print(f"\nSoma das razões (n_ij / t_ij) = {sum_ratios:.4f}")
    print(f"Denominador (R*N) = {R} * {N} = {R*N}")
    print("========================================\n")
    # --- Fim das impressões de depuração ---

    return tbe
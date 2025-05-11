import pandas as pd
import argparse
from gerar_metricas.metrics import *

def main():

    parser = argparse.ArgumentParser(
        description="Gera metricas IHC a partir do arquivo CSV."
    )
    parser.add_argument(
        "--csv",
        type=str,
        required=True,
        help="Caminho para o arquivo CSV com os dados."
    )
    args = parser.parse_args()
    
    df = pd.read_csv(args.csv, encoding='utf-8-sig')

    comparar_tbe_com_otimo(df)
    #pa = calcular_pa(args.csv)
    #print(f"Percentual de Ajuda Solicitada ou Necessária")
    #print("------------------------------")
    #print(f"PA: {pa:.2f}%")
    #print("------------------------------")
  
   
def completion_rate(df: pd.DataFrame):
    """
    Calcula a taxa de conclusão de tarefas e exibe os resultados.
    """
    overall_rate, per_resident = calculate_completion_rate(df)

    print("\nTaxa de Conclusão de Tarefas")
    print("------------------------------")
    print(f"Taxa Geral: {overall_rate:.2f}%")
    print("\nTaxa por Residente:")
    print(per_resident.to_string())

def average_time(df: pd.DataFrame):
    """
    Calcula e exibe o Tempo Médio Geral, por Residente e por Tarefa.
    Os valores são exibidos em segundos.
    """
    avg_overall, avg_by_resident, avg_by_task = calculate_average_time(df)

    print("\nTempo Médio (em segundos)")
    print("-------------------------")

    print(f"Tempo Médio Geral: {avg_overall:.2f} s")

    print("\nTempo Médio por Residente:")

    for residente, tempo in avg_by_resident.items():
        print(f"  {residente}: {tempo:.2f} s")

    print("\nTempo Médio por Tarefa:")
    for tarefa, tempo in avg_by_task.items():
        print(f"  {tarefa}: {tempo:.2f} s")

def error_rate(df: pd.DataFrame):
    """
    Calcula e exibe a Taxa de Erros, considerando cada tarefa (iteraçao).
    """
    overall_rate, rate_by_resident = calculate_error_rate(df)
    
    print("\nTaxa de Erros (por tarefa)")
    print("------------------------------")
    print(f"Taxa Global de Erros: {overall_rate:.2f}%")
    print("\nTaxa de Erros por Residente:")
    for residente, taxa in rate_by_resident.items():
        print(f"  {residente}: {taxa:.2f}%")

def learning_rate(df: pd.DataFrame):
    """
    Calcula a taxa de aprendizagem e exibe os resultados no CMD.
    Também gera um gráfico de barras para visualizar a taxa de aprendizagem por residente.
    """
    learning_rate_by_resident, overall_learning_rate = calculate_learning_rate(df)

    print(f"\nTaxa de Aprendizagem entre Tarefa 1 + 2 e Tarefa 6")
    print("---------------------------------------------------------")
    print(f"Taxa de Aprendizagem Geral: {overall_learning_rate:.2f}%\n")

    for residente, taxa in learning_rate_by_resident.items():
        print(f"  {residente}: {taxa:.2f}%")

def completion_rate(df: pd.DataFrame):
    """
    Exibe a Eficiência Baseada no Tempo (TBE),
    calculada como a média das razões n_ij / t_ij.
    """
    tbe_value = calculate_completion_rate(df)
    print("Eficiência Baseada no Tempo (TBE) - Média das razões n_ij / t_ij")
    print("----------------------------------------------------------------")
    print(f"TBE (valor decimal) = {tbe_value:.4f}")
    print(f"TBE (percentual)    = {tbe_value * 100:.2f}%")


if __name__ == "__main__":
    main()

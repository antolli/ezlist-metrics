import argparse
import pandas as pd
from gerar_graficos.converter import converter_excel_para_csv
from gerar_graficos.plotting import plot_duration_with_means, plot_duration, plot_event_frequency

def main():
    parser = argparse.ArgumentParser(description="Ferramenta para converter dados e gerar gráficos.")
    parser.add_argument("--excel", type=str, help="Caminho para o arquivo Excel a ser convertido.")
    parser.add_argument("--csv", type=str, help="Caminho para salvar o CSV convertido ou para o CSV existente.")
    parser.add_argument("--grafico", type=str, choices=["duration", "barras"], help="Tipo de gráfico a ser plotado.")
    args = parser.parse_args()
    
    # Se o parâmetro --excel for fornecido, realiza a conversão
    if args.excel:
        if not args.csv:
            print("Informe o caminho para salvar o CSV com --csv.")
            return
        print("Convertendo arquivo Excel para CSV...")
    
        converter_excel_para_csv(args.excel, args.csv, encoding="utf-8-sig")
        print("Conversão concluída.")
    
    # Se o parâmetro --grafico for informado, tenta carregar o CSV e plotar o gráfico
    if args.grafico:
        if not args.csv:
            print("Para plotar um gráfico, informe o caminho para o CSV com --csv")
            return
        try:
            df = pd.read_csv(args.csv, encoding="utf-8-sig")
        except Exception as e:
            print(f"Erro ao ler o CSV: {e}")
            return
        if args.grafico == "duration":
            plot_duration_with_means(df)
        elif args.grafico == "barras":
            plot_event_frequency(df)

if __name__ == "__main__":
    main()

import pandas as pd

def converter_excel_para_csv(excel_path: str, output_csv: str, encoding: str='utf-8') -> None:
    """
    Lê todas as abas do arquivo Excel, concatena-as em um único DataFrame e salva em CSV.
    
    Args:
        excel_path (str): Caminho para o arquivo Excel.
        output_csv (str): Caminho para o arquivo CSV de saída.
        encoding (str, optional): Codificação para o CSV. Padrão é 'utf-8'.
    """
    sheets = pd.read_excel(excel_path, sheet_name=None)
    df_total = pd.concat(sheets.values(), ignore_index=True)
    df_total.to_csv(output_csv, index=False, encoding=encoding)
    print(f"Arquivo CSV salvo em {output_csv}.")

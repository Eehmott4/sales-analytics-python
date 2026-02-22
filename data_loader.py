import pandas as pd
from sqlalchemy import create_engine


REQUIRED_COLUMNS = [
    'id_venda',
    'data_venda',
    'cliente_id',
    'produto',
    'quantidade',
    'preco_unit',
    'valor_total'
]


def validate_schema(df: pd.DataFrame):
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    return True


def standardize_data(df: pd.DataFrame):
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')

    df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
    df['preco_unit'] = pd.to_numeric(df['preco_unit'], errors='coerce')
    df['valor_total'] = pd.to_numeric(df['valor_total'], errors='coerce')

    return df

def load_csv(file_path):
    df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("COLUNAS NORMALIZADAS:", df.columns.tolist())

    validate_schema(df)
    df = standardize_data(df)
    return df

def load_excel(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    validate_schema(df)
    df = standardize_data(df)
    return df


def load_sql(user: str, password: str, host: str, database: str) -> pd.DataFrame:
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    query = "SELECT * FROM vendas"
    df = pd.read_sql(query, engine)
    validate_schema(df)
    df = standardize_data(df)
    return df

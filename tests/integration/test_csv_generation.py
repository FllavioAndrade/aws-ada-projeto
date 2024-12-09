import pytest
import pandas as pd
import os
from app.main import criar_csv

def test_csv_format_and_content():
    # Testa geração e formato do CSV
    filename = criar_csv()
    
    # Verifica se arquivo foi criado
    assert os.path.exists(filename)
    
    # Lê o CSV e verifica estrutura
    df = pd.read_csv(filename)
    required_columns = ['ID', 'Salario', 'Admissao', 'Setor']
    
    # Verifica colunas
    for col in required_columns:
        assert col in df.columns
    
    # Verifica tipos de dados
    assert df['ID'].dtype == 'int64'
    assert df['Salario'].dtype == 'float64'
    
    # Limpa arquivo de teste
    os.remove(filename)
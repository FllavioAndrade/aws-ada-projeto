import pytest
from datetime import datetime
from app.main import gerar_dados_aleatorios, criar_csv
import os

def test_gerar_dados_aleatorios():
    # Teste com número fixo de linhas
    num_rows = 5
    data = gerar_dados_aleatorios(num_rows)
    
    assert len(data) == num_rows
    for row in data:
        assert 'ID' in row
        assert 1000 <= row['ID'] <= 9999
        assert 'Salario' in row
        assert 10.0 <= row['Salario'] <= 1000.0
        assert 'Admissao' in row
        assert 'Setor' in row
        assert row['Setor'] in ['DevOps', 'SRE', 'Funcionário_ADA', 'DevSecOps']

def test_criar_csv():
    filename = criar_csv()
    assert os.path.exists(filename)
    assert filename.startswith('contabil_')
    assert filename.endswith('.csv')
    os.remove(filename)  # Limpa após o teste
import csv
import random
from datetime import datetime, timedelta

def gerar_dados_aleatorios(num_rows):
    data = []
    current_date = datetime.now()
    
    for _ in range(num_rows):
        row = {
            'ID': random.randint(1000, 9999),
            'Salario': round(random.uniform(10.0, 1000.0), 2),
            'Admissao': (current_date - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'Setor': random.choice(['DevOps', 'SRE', 'Funcionário_ADA', 'DevSecOps'])
        }
        data.append(row)
    
    return data

def criar_csv():
    num_rows = random.randint(0, 100)
    data = gerar_dados_aleatorios(num_rows)
    
    filename = f'contabil_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Salario', 'Admissao', 'Setor']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Criando Arquivo CSV '{filename}' com {num_rows} linhas")
    return filename
##
if __name__ == "__main__":
    criar_csv()
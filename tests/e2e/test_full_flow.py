import pytest
import boto3
import psycopg2
from app.main import criar_csv
import os

@pytest.mark.e2e
def test_full_process():
    # 1. Gera CSV
    filename = criar_csv()
    assert os.path.exists(filename)
    
    # 2. Upload para S3
    s3 = boto3.client('s3')
    bucket_name = "ada-contabil-1182"
    try:
        s3.upload_file(filename, bucket_name, filename)
        
        # 3. Verifica se arquivo está no S3
        response = s3.head_object(Bucket=bucket_name, Key=filename)
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200
        
        # 4. Espera processamento (pode precisar ajustar o tempo)
        import time
        time.sleep(10)
        
        # 5. Verifica no banco de dados
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        cur = conn.cursor()
        
        cur.execute(
            "SELECT * FROM arquivos_processados WHERE nome_arquivo = %s",
            (filename,)
        )
        result = cur.fetchone()
        assert result is not None
        
        cur.close()
        conn.close()
        
    finally:
        # Limpa arquivos de teste
        os.remove(filename)
        s3.delete_object(Bucket=bucket_name, Key=filename)
#Cria um bucket S3 para armazenar os arquivos da contabilidade
resource "aws_s3_bucket" "bucket_contabil" {
  bucket = "ada-contabil-1182"
  force_destroy = true
}
#Bloqueia o acesso público ao bucket
resource "aws_s3_bucket_public_access_block" "acesso_bucket" {
  bucket = aws_s3_bucket.bucket_contabil.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

#Cria um bucket S3 para armazenar o estado do Terraform
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-ada-1182"
  force_destroy = true
}
#Bloqueia o acesso público ao bucket
resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Notificação do S3 para SNS quando arquivo é criado
resource "aws_s3_bucket_notification" "notifica_upload" {
  bucket = aws_s3_bucket.bucket_contabil.id

  topic {
    topic_arn = aws_sns_topic.upload_do_arquivo.arn
    events    = ["s3:ObjectCreated:*"]
  }
}

#Cria um arquivo de output com o nome do bucket criado
output "bucket_contabil_name" {
  value       = aws_s3_bucket.bucket_contabil.id
  description = "Nome do bucket contábil"
}

output "bucket_state_name" {
  value       = aws_s3_bucket.terraform_state.id
  description = "Nome do bucket de estado do Terraform"
}
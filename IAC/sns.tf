#Cria um tópico no SNS
resource "aws_sns_topic" "upload_do_arquivo" {
  name = "arquivo-contabil-carregado"
}

# Política para permitir que o S3 publique no SNS
resource "aws_sns_topic_policy" "default" {
  arn = aws_sns_topic.upload_do_arquivo.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action   = "SNS:Publish"
        Resource = aws_sns_topic.upload_do_arquivo.arn
        Condition = {
          StringEquals = {
            "aws:SourceAccount": data.aws_caller_identity.current.account_id
          },
          ArnLike = {
            "aws:SourceArn": aws_s3_bucket.bucket_contabil.arn
          }
        }
      }
    ]
  })
}

# Para obter o ID da conta AWS atual
data "aws_caller_identity" "current" {}
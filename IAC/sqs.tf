# cria um SQS
resource "aws_sqs_queue" "processa_arquivo" {
  name = "process-arquivo-contabil"
  visibility_timeout_seconds = 60
}

resource "aws_sns_topic_subscription" "sqs_subscription" {
  topic_arn = aws_sns_topic.upload_do_arquivo.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.processa_arquivo.arn
}

# SQS Queue Policy
resource "aws_sqs_queue_policy" "politica_processa_arquivo" {
  queue_url = aws_sqs_queue.processa_arquivo.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "sns.amazonaws.com"
        }
        Action   = "sqs:SendMessage"
        Resource = aws_sqs_queue.processa_arquivo.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn": aws_sns_topic.upload_do_arquivo.arn  # Corrigido para match com o nome do tópico SNS
          }
        }
      }
    ]
  })
}
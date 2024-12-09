import pytest
import json
from app.lambda_function import count_lines, lambda_handler
from unittest.mock import MagicMock, patch

def test_count_lines():
    # Simula cliente S3
    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {
        'Body': MagicMock(
            read=lambda: b"linha1\nlinha2\nlinha3"
        )
    }
    
    count = count_lines(mock_s3, "bucket-test", "file.csv")
    assert count == 3

@patch('app.lambda_function.save_to_db')
def test_lambda_handler(mock_save_to_db):
    # Simula evento do SQS/SNS
    event = {
        "Records": [{
            "body": json.dumps({
                "Message": json.dumps({
                    "Records": [{
                        "s3": {
                            "bucket": {"name": "test-bucket"},
                            "object": {"key": "test.csv"}
                        }
                    }]
                })
            })
        }]
    }
    
    with patch('app.lambda_function.boto3.client') as mock_boto:
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {
            'Body': MagicMock(
                read=lambda: b"linha1\nlinha2\nlinha3"
            )
        }
        mock_boto.return_value = mock_s3
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 200
        mock_save_to_db.assert_called_once_with("test.csv", 3)
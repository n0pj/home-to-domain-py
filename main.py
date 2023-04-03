import os
import boto3
import requests
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込む
load_dotenv()

# IP を取得する API の URL
ip_api_url = "https://inet-ip.info/ip"

# AWS のアクセスキー ID とシークレットアクセスキー
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

# ドメイン名とホストゾーン ID
domain_name = os.environ.get("DOMAIN_NAME")
hosted_zone_id = os.environ.get("HOSTED_ZONE_ID")

# IP を取得
response = requests.get(ip_api_url)
ip_address = response.text

# Route 53 に登録するリソースレコードの値
resource_record_value = {"Value": ip_address}

# Boto3 セッションを作成
session = boto3.Session(
    aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key
)

# Route 53 クライアントを作成
client = session.client("route53")

# ドメインのリソースレコードを更新
response = client.change_resource_record_sets(
    HostedZoneId=hosted_zone_id,
    ChangeBatch={
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": domain_name,
                    "Type": "A",
                    "TTL": 300,
                    "ResourceRecords": [resource_record_value],
                },
            }
        ]
    },
)

print(response)

import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from Configurations.config import AppConfig


class SendFile:
    @staticmethod
    def send_file_to_slack(file_path):
        client = WebClient(token=AppConfig.NOTIFICATION.SLACK_TOKEN)
        try:
            with open(file_path, "rb") as file_content:
                response = client.files_upload_v2(
                    channel=AppConfig.NOTIFICATION.SLACK_CHANNEL_ID,
                    file=file_content,
                    title="Generated Report",
                    initial_comment="Test Report",
                    filename="report.csv",
                )
            print(f"File uploaded successfully: {response['file_id']}")
        except SlackApiError as e:
            print(f"Error uploading file: {e.response['error']}")

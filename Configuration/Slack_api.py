import pandas as pd
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SLACKAPI:
    slack_token = "xoxb-35910659621-8102197763670-5YPBpmVlVEBhKkUciaObjnrn"
    channel_id = "C06RBC6UZRC"

    def send_file_to_slack(self, file_path):
        client = WebClient(token=SLACKAPI.slack_token)
        try:
            with open(file_path, "rb") as file_content:
                response = client.files_upload_v2(
                    channels=SLACKAPI.channel_id,
                    file=file_content,
                    title="Generated Report",
                    initial_comment="Test Report",
                    filename="report.csv",
                    filetype="csv"
                )
            print(f"File uploaded successfully: {response['file_id']}")
        except SlackApiError as e:
            print(f"Error uploading file: {e.response['error']}")

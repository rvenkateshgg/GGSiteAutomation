import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from Configurations.config import AppConfig


# Sets the debug level.
# If you're using this in production, you can change this back to INFO and add extra log entries as needed.
# logging.basicConfig(level=logging.DEBUG)
#
# # Initialize the Web API client.
# # This expects that you've already set your SLACK_BOT_TOKEN as an environment variable.
# # Try to resist the urge to put your token directly in your code; it is best practice not to.
#
#
# os.environ["SLACK_BOT_TOKEN"] = SLACKAPI.slack_token
# client = WebClient(os.environ["SLACK_BOT_TOKEN"])
#
# # Tests to see if the token is valid
# auth_test = client.auth_test()
# bot_user_id = auth_test["user_id"]
# print(f"App's bot user: {bot_user_id}")
#

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

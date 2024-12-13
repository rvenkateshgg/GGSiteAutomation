import time
import pandas as pd
from Utilities.slackUtils import SendFile
from Configurations.report_config import ReportConfig


def get_report():
    broken_url = []
    if broken_url:
        df = pd.DataFrame(broken_url, columns=["URL", "Status Code"])
        df.to_csv(ReportConfig.REPORT_PATH, index=False)
        SendFile.send_file_to_slack(ReportConfig.REPORT_PATH)

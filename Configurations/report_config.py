import os


class ReportConfig:
    REPORT_PATH = '../Reports/brokenlink.csv'
    report_dir = os.path.abspath('../Reports')
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

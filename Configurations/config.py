from Configurations.gg_shopify_config import GGShopifyConfig
from Configurations.gg_site_config import GGSiteConfig
from Configurations.notification_config import NotificationConfig
from Configurations.report_config import ReportConfig


class AppConfig:
    NOTIFICATION = NotificationConfig
    REPORT = ReportConfig
    GG_SITE = GGSiteConfig
    GG_SHOPIFY = GGShopifyConfig

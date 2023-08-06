from extras.plugins import PluginConfig

class DeviceScannerConfig(PluginConfig):
    name = 'netbox-device-scan',
    verbose_name = 'Device Scanner',
    decription = 'A Netbox plugin for device scanning',
    version = '0.1',
    author = 'Sean Collins',
    author_email = 'collsean@umich.edu',
    base_url = 'device-scan',
    required_settings = []

config = MacScannerConfig
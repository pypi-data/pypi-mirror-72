from extras.plugins import PluginConfig

class DeviceScannerConfig(PluginConfig):
    name = 'netbox_plugin_test',
    verbose_name = 'Plugin Tester',
    decription = 'A Netbox plugin test',
    version = '0.3',
    author = 'Sean Collins',
    author_email = 'collsean@umich.edu',
    base_url = 'plugin-test',
    required_settings = []

config = DeviceScannerConfig

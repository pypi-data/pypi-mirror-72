from setuptools import find_packages, setup

setup(
    name='netbox-mac-scan',
    version='0.1',
    description='A Netbox plugin for MAC address scanning',
    url='https://github.com/seanmcollins/netbox-mac-scan',
    author='Sean Collins',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
)
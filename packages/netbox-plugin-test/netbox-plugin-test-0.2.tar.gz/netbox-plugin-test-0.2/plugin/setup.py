from setuptools import find_packages, setup

setup(
    name='netbox-plugin-test',
    version='0.2',
    description='A Netbox plugin test',
    author='Sean Collins',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
)
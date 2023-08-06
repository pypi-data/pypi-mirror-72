import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='netbox-plugin-test',
    version='0.3',
    description='A Netbox plugin testing build',
    author='Sean Collins',
    install_requires=[],
    packages=setuptools.find_packages(),
    include_package_data=True,
)

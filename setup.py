from setuptools import find_packages, setup

setup(
    name='PyComm',
    packages=find_packages(include=['PyComm']),
    version='0.1.0',
    description='An encrypted TCP communication libarary',
    author='Anish Sharma',
    license='GPLv3-or-later',
    install_requires=['cryptography']
)

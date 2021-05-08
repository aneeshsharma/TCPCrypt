from setuptools import find_packages, setup

setup(
    name='pycomm',
    packages=find_packages(include=['pycomm']),
    version='0.1.0',
    description='An encrypted TCP communication libarary',
    author='Anish Sharma',
    license='GPLv3.0-or-later',
    install_requires=['cryptography']
)

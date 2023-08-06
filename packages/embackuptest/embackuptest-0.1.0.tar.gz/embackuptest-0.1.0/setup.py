from setuptools import setup, find_packages
setup(
    name='embackuptest',
    version='0.1.0',
    description='Experimental package for RDS backup',
    url='https://github.com/emiksa/backup-script',
    install_requires=['boto3', 'click'],
    author='Ernestas Miksa',
    author_email='kinkan@yandex.com',
    packages=['embackuptest']
)

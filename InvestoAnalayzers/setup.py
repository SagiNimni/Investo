from setuptools import find_packages, setup

with open('requirements.txt', encoding='utf16') as dependencies:
    dependencies = dependencies.read().split("\n")

setup(
    name='InvestoAnalayzers',
    packages=find_packages(include=find_packages()),
    version='1.0',
    description='This library contains some analayzers that evaluate stocks',
    author='Sagi Nimni',
    license='MIT',
    install_requires=dependencies
)
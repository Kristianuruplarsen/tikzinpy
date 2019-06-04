from setuptools import setup, find_packages


setup(
    name = 'tikzinpy',
    version = '0.1',
    author = 'Kristian Olesen Larsen',
    description = 'A plotting library that uses tikz as its backend',
    url='https://github.com/Kristianuruplarsen/tikzinpy',
    packages = find_packages(),
    install_requires = ['numpy', 'matplotlib']
)
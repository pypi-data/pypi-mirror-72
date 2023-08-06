from setuptools import setup

setup(
    name='parser_libraries',
    version='1.7',
    packages=['parser_libraries'],
    author_email='ivan.frinom@gmail.com',
    install_requires=[
        'pymysql',
        'openpy',
        'requests'
    ]
)

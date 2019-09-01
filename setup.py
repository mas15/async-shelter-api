from setuptools import setup, find_packages

setup(
    name='shelter_asyncio',
    entry_points={
        'console_scripts': [
            'api=shelter.service:main'
        ],
    },
    install_requires=[
        'aiobotocore==0.10.3',
        'aiohttp==3.5.4',
        'gino==0.8.3',
        'SQLAlchemy==1.3.8'
    ],
    version='0.1',
    packages=find_packages()
)

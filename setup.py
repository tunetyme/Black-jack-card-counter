from setuptools import setup, find_packages

setup(
    name='BlackjackCardCounter',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyQt5==5.15.7',
    ],
    entry_points={
        'console_scripts': [
            'blackjack-counter=main:main',
        ],
    },
)

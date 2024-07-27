from setuptools import setup, find_packages

setup(
    name='BlackjackCardCounter',
    version='1.0',
    packages=find_packages(),
    package_data={'': ['*.py']},  # Include all .py files
    install_requires=[
        'PyQt5==5.15.7',
    ],
    entry_points={
        'console_scripts': [
            'blackjack-counter=BlackjackCardCounter.main:main',
        ],
    },
)

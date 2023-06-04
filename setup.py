from setuptools import setup, find_packages

setup(
    name="scraping_logs",
    version="0.1",
    packages=find_packages(),
    license="MIT",
    entry_points={
        'console_scripts': [
            'project_name = scraping_logs.main:main'
        ]
    },
)

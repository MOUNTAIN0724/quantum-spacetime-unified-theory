from setuptools import setup, find_packages

setup(
    name="qst-theory",
    version="0.1.0",
    description="Quantum Space-Time Unified Theory Framework",
    author="QST Research Team",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
    ],
)

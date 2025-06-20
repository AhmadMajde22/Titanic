from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "Titanic-Survaival",
    version = "0.5",
    author = "Ahmad Majdi",
    packages = find_packages(),
    install_requires = requirements
)

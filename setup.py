from setuptools import setup

setup(
    name="podio-mirror",
    version="0.1",
    description="Wrapper for part of the Podio API with interfaces for caching data locally",
    author="Patrik Sletmo",
    author_email="patrik.sletmo@gmail.com",
    url="https://github.com/patriksletmo/podio-mirror",
    license="MIT",
    packages=["podiomirror"],
    install_requires=["requests"]
)

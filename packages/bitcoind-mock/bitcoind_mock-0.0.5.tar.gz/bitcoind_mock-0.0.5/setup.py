import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="bitcoind_mock",
    version="0.0.5",
    author="Sergi Delgado Segura",
    author_email="sergi.delgado.s@gmail.com",
    description="A tiny and non-exhaustive mock for bitcoind",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sr-gi/bitcoind_mock",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["zmq", "networkx", "flask", "requests", "riemann-tx==2.1.0"],
    python_requires=">=3.6",
)

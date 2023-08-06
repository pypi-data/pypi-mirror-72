from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name="algobin",
    version="0.0.1",
    description="Basic trading operations of binance to be used in algorithmic trading.",
    py_modules=["algobin"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = ['algoutils', 'requests', 'urllib', 'hmac', 'hashlib',],
    extras_require = {
        "dev" : [
            "pytest>=3.7",
        ],
    },
    url="https://github.com/aticio/algobin",
    author="Özgür Atıcı",
    author_email="aticiozgur@gmail.com",
)
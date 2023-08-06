from setuptools import setup

setup(
    name="Jixin",
    version="1.0.0",
    author="Adam Faulconbridge",
    author_email="afaulconbridge@googlemail.com",
    packages=["jixin"],
    description="JSON (de)serialization mix-ins.",
    long_description=open("README.md").read(),
    url='https://github.com/afaulconbridge/jixin',
    license='LICENSE.txt',
    install_requires=[""],
    extras_require={
        "dev": [
            "pytest-cov",
            "flake8",
            "black",
            "pylint",
            "pip-tools",
            "pipdeptree",
            "pre-commit",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

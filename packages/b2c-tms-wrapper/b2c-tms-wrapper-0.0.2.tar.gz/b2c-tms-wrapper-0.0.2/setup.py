from setuptools import setup, find_packages

setup(
    name="b2c-tms-wrapper",
    version="0.0.2",
    description="Interface for b2c_tms backend",
    url="https://github.com/shuttl-tech/b2c-tms-wrapper",
    author="Shuttl",
    author_email="author@example.com",
    license="MIT",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.7"],
    install_requires=["pytz"],
    extras_require={
        "test": [
            "pytest",
            "pytest-runner",
            "pytest-cov",
            "pytest-pep8",
            "requests",
            "responses",
            "pyshuttlis",
        ],
        "dev": ["flake8"],
    },
)

from setuptools import setup, find_packages

setup(
    name="inversion",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "optuna",
        "pyarrow",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Bayesian inversion package for model optimization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
) 
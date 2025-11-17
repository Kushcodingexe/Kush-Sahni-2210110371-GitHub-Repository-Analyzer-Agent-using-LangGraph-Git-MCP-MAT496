"""Setup script for GitHub Repository Analyzer Agent."""
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="github-agent",
    version="0.1.0",
    description="AI agent for GitHub repository analysis and issue investigation",
    author="Your Name",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "github-agent=src.cli:cli",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)

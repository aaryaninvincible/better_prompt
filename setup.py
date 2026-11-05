from setuptools import setup, find_packages

setup(
    name="better-prompt",
    version="1.0.0",
    description="Intelligent multi-language prompt engineering tool",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "better-prompt=better_prompt.cli:main",
        ],
    },
)

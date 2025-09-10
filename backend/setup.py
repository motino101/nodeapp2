from setuptools import setup, find_packages

setup(
    name="content-maker",
    version="1.0.0",
    description="AI-powered content creation system",
    author="Content Maker Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "tensorzero",
        "requests",
        "beautifulsoup4",
        "pathlib",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "content-maker=content_maker.core.main:main",
        ],
    },
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langchain-deck",
    version="0.1.0",
    author="Eric",
    author_email="616920675@qq.com",
    description="A CSS-first, native PPTX rendering engine for AI Agents.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eric910630/Deck",
    project_urls={
        "Bug Tracker": "https://github.com/Eric910630/Deck/issues",
        "Source Code": "https://github.com/Eric910630/Deck",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: LangChain",
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "python-pptx>=0.6.21",
        "playwright>=1.40.0",
        "loguru>=0.7.0",
        "webcolors>=1.13",
        "pydantic>=2.0.0",
        "openai>=1.0.0",
        "matplotlib>=3.7.0",
        "pandas>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "deck=deck_cli:main",
        ],
    },
    include_package_data=True,
)


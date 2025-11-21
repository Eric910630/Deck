from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = [line.strip() for line in f.read().splitlines() if line.strip() and not line.startswith("#")]

setup(
    name="langchain-deck",
    version="0.1.2",
    author="Eric",
    author_email="616920675@qq.com",
    description="A tool to automatically generate PPT decks using LangChain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eric910630/Deck",
    project_urls={
        "Bug Tracker": "https://github.com/Eric910630/Deck/issues",
        "Source Code": "https://github.com/Eric910630/Deck",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "deck=langchain_deck.deck_cli:main",
        ],
    },
    python_requires=">=3.8",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    include_package_data=True,
)

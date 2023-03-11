from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "WinterHackhatonFCT"
AUTHOR_USER_NAME = "RodrigoRalhaMoreira"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = ['streamlit', 'numpy', 'seaborn']


setup(
    name=SRC_REPO,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    description="A small package for Movie Recommender System :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="rr.moreira@campus.fct.unl.pt",
    packages=[SRC_REPO],
    license="MIT",
    python_requires=">=3.9",
    install_requires=LIST_OF_REQUIREMENTS
)
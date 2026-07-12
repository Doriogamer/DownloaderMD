from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="downloadMD",
    version="1.0.0",
    author="Doriogamer",
    author_email="dalvarezwallace2@gmail.com",
    description="Descargador universal para YouTube, MP3 y links directos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Doriogamer/DownloaderMD",
    py_modules=["downloader"],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "downloadermd=downloader:__main__",
        ],
    },
)

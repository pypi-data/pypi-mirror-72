from sys import executable
from os import system
from setuptools import setup
from os import remove

# put shebang
lines = open("7pack.py").read().split("\n")
lines.insert(0, "#!" + executable)
lines = "\n".join(lines)
with open("7pack", "w+") as f:
    f.write(lines)
    system("chmod +x " + "7pack")

with open("README.md", "r") as fh:
    long_description = fh.read()

# Run Setup
setup(name="7pack",
      install_requires=["certifi", "chardet", "gitdb", "GitPython", "idna", "requests", "smmap", "urllib3"],
      scripts=["7pack", "indexed.json"],
      python_requires='>=3.6',
      url="https://github.com/Nv7-GitHub/7pack_Code",
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: MacOS",
        ],
      version="0.0.1",
      author="Nishant Vikramaditya",
      author_email="junk4Nv7@gmail.com",
      )
remove("7pack")

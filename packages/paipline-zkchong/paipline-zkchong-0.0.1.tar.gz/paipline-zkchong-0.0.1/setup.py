import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paipline-zkchong", # Replace with your own username
    version="0.0.1",
    author="Zan-Kai Chong",
    author_email="zkchong@gmail.com",
    description="Simple pipeline alternative to Scikit Learn's Pipeline.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zkchong/Paip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.0',
)
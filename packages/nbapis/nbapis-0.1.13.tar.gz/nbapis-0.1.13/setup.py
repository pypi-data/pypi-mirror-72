import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nbapis",  # Replace with your own username
    version="0.1.13",
    author="zhchangAuthor",
    author_email="chang@nextbillion.ai",
    description="nb api package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'fastapi>=0.53.1'
    ],
    python_requires='>=3.6',
    include_package_data=True,
)

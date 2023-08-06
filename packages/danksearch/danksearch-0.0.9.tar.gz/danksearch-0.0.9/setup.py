import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="danksearch", 
    version="0.0.9",
    author="DankCoder",
    author_email="business.dankcoder@gmail.com",
    description="An async youtube search library made for use with discord.py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/actualdankcoder/danksearch-discord",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["aiohttp","lxml"],
    include_package_data=True
)
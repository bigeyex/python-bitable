import setuptools

with open("./README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitable",
    version="1.0.3",
    author="Yu Wang (bigeyex)",
    author_email="bigeyex@gmail.com",
    description="A Python package to operate with Feishu/Lark bitable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bigeyex/python-bitable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests==2.32.3",
    ],
    include_package_data = True,
    python_requires='>=3.6',
)
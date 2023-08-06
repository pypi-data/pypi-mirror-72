import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyForSatan",  # Replace with your own username
    version="0.0.2",
    author="Satan",
    author_email="satanwuming@gmail.com",
    description="a tools package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/satanwuming/PyForSatan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
        'paramiko>=2.4.2',
        'paramiko>=2.4.2',
        'openpyxl>=2.5.6',
        'xlrd>=1.1.0',
        'PyYAML>=5.1.2'
    ]
)

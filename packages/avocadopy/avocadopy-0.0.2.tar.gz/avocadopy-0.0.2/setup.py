import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="avocadopy",
    version="0.0.2",
    author='B Niu',
    author_email='shinji006@126.com',
    description='Tools for medical statistics.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/b-niu/avocadopy',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

from setuptools import *

with open("README.md", "r") as r:
    long_description = r.read()

setup(
    name="frpy", # Replace with your own username
    version="0.0.6",
    author="Calculus",
    author_email="calculus0972@gmail.com",
    description="An api for FRHD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/frpy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ],
    python_requires='>=3.8'
)

# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository pypi dist/*
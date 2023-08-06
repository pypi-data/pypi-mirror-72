
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pingy",
    version="0.0.0",
    author="Sajjad alDalwachee",
    author_email="iamsajjad@mail.ru",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'Click',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
    ''',
    python_requires='>=3.6',
)


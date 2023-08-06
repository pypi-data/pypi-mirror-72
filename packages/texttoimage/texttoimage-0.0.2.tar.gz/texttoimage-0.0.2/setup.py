import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="texttoimage", # Replace with your own username
    version="0.0.2",
    author="Jeffrey Hu",
    author_email="zhiwehu@gmail.com",
    description="Texttoimage is a Python library for converting text to a transparent image.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhiwehu/texttoimage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['Pillow', 'fonts', 'font-roboto'],
    python_requires='>=3.6',
)
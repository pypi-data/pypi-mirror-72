import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="haxor-game", # Replace with your own username
    version="0.0.1",
    author="Angel Davila",
    author_email="",
    description="How good are you at haxoring?",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adavila0703/haxor-game-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.8',
)

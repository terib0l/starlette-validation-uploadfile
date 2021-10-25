from setuptools import setup

VERSION = "0.1.1"

def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()

setup(
    name="starlette-validation-uploadfile",
    version=VERSION,
    license="MIT",
    description="Middleware for validation upload-file in FastAPI and Starlette.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="terib0l",
    url="https://github.com/terib0l/starlette-validation-uploadfile",
    python_requires=">=3.6",
    py_modules=["starlette_validation_uploadfile"],
    keywords="starlette fastapi middleware upload file validation",
    install_requires=["starlette>=0.12.11"],
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)

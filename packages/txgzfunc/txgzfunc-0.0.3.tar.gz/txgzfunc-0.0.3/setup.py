import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="txgzfunc",
    version="0.0.3",
    author="txgz",
    author_email="975663670@qq.com",
    description="tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/txgzlyy/txgz_func",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'docx',
        'pypiwin32'
    ],
    python_requires='>=3.6',
)

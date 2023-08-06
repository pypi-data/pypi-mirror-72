import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blacktip",
    version="0.0.6",
    author="Matt Beveridge",
    author_email="mattjbev@gmail.com",
    description="SEC Edgar Analysis Tools (by Blacktip Research)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://blacktipresearch.com/Angler",
    keywords=["SEC", "edgar", "finance", "10-K", "10-Q"],
    install_requires=[
        "requests",
        "pandas",
        "sqlalchemy",
        "pymysql"
    ],
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

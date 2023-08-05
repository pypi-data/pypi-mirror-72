import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="comapsmarthome-orm-utils",
    version="0.1.0",
    author="Aurélien Sylvan",
    author_email="aurelien.sylvan@comap.eu",
    description="ORM stuff for ComapSmartHome",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=["test"]),
    install_requires=[
        'psycopg2-binary>=2.8.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

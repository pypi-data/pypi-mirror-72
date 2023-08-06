import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-randomcharfield",
    version="0.0.1",
    author="Yoong Kang Lim",
    author_email="yoongkang.lim@gmail.com",
    description="An alternative to UUIDs for model fields",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoongkang/django-charfield",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['django>=2.2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

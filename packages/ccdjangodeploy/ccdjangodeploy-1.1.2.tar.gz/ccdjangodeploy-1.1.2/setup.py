from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="ccdjangodeploy",
    version="1.1.2",
    description="A Python package to deploy django project on any linux based system.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/avinashkatariya/ccdjangodeploy",
    author="Avinash Katariya",
    author_email="avinashkatariya@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ccdjangodeploy"],
    include_package_data=True,
    install_requires=[""],
    entry_points={
        "console_scripts": [
            "ccdd=ccdjangodeploy.cli:main",
            "updateccdd=ccdjangodeploy.update:update"
        ]
    },
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gugong", # Replace with your own username
    version="0.5.5",
    author="Robert Wen",
    author_email="saphires@163.com",
    description="Data library for GuGong, a.k.a as The Palace Museum or The Fobidden City",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robertwenquan/gugong",
    packages=['gugong'],
    package_dir={'gugong': 'gugong'},
    package_data={'gugong': ['data/gugong.json', 'proto/*.py', 'models/*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

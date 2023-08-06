from setuptools import setup, find_packages


setup(
    name="basic_card-hannu_hell", 
    version="0.0.1",
    author="Hanoon Malik",
    author_email="hannu_hell@hotmail.com",
    description="Basic card game functions",
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hannu-hell/basic_card",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

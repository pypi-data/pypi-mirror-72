from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="markable",
    version="1.0.1",
    author="Ron Chang",
    author_email="ron.hsien.chang@gmail.com",
    description="Print out colorful text.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ron-Chang/markable",
    packages=find_packages(),
    license='MIT',
    python_requires='>=3',
    exclude_package_date={'': ['.gitignore', 'dev', 'test', 'setup.py']},
)

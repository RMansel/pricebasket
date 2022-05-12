from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as handle:
    long_desc = handle.read()

with open("requirements.txt", "r", encoding="utf-8") as handle:
    reqs = handle.read()

setup(
    name='mytool',
    version='0.0.1',
    author='Rhys Mansel',
    author_email='r.mansel@perceivedata.com',
    license='MIT',
    description='an example command line tool for calculating the cost of a basket of goods',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    py_modules=['main', 'pricebasket'],
    packages=find_packages(),
    install_requires=[reqs],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        PriceBasket=main:cli
    '''
)

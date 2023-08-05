import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires = [
    'python-dateutil==2.8.1'
]

setuptools.setup(
    name='dnx-data', # Replace with your own username
    version='0.1.4',
    author='DNX Solutions',
    author_email='contact@dnx.solutions',
    description='DNX data solution package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DNXLabs/dnx-data',
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
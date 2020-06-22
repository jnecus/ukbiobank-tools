# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

	
def list_requirements():
    with open('requirements.txt', 'r') as f:
        reqs = [line.strip() for line in f]
        return reqs 
		
	
	
	
setup(
    name='ukbiobank-tools',
    version='0.1.7',
    description='Useful tools for working with UK Biobank meta-data',
    author='Joe Necus',
    author_email='joenecus@gmail.com',
    url='https://github.com/jnecus/ukbiobank-tools',
    license=license,	
	packages=find_packages(include=["ukbiobank"]),
    package_data={"": ["data_coding/*"]},
	install_requires=list_requirements()
)


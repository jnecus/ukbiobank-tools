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
    version='0.1.1',
    description='Useful tools for working with UK Biobank meta-data',
    author='Joe Necus',
    author_email='joenecus@gmail.com',
    url='https://github.com/jnecus/ukbiobank-tools',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
	package_data = {'ukbiobank/data_coding': ['*']},
	install_requires=list_requirements()
)

#package_data = {'ukbiobank/data_coding': ['*']}
#This line causes data_coding to be included as a package (it would normally be one of the folders ignored by find_packages
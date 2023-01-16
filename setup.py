from setuptools import setup, find_packages

setup(
    name='dmm2bm',
    version=open('VERSION').read().strip(),
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/xray-imaging/dmm2bm',
    packages=find_packages(where="dmm2bm"),
    package_dir={"": "dmm2bm"},
    package_data={"dmm2bm": ["*.json", ]},
    include_package_data = True,
    scripts=['bin/dmm'],
    description='Utitlity to change the DMM energy at 2-BM',
    zip_safe=False,
)


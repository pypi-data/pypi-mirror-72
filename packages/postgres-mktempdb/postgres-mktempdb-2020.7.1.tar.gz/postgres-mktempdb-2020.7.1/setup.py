import setuptools

setuptools.setup(
    name='postgres-mktempdb',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/mktempdb']
)

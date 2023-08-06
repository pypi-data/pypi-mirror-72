import setuptools

setuptools.setup(
    name='temp-untar',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/temp-untar']
)

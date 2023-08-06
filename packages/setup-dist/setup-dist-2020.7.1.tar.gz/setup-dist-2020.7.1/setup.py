import setuptools

setuptools.setup(
    name='setup-dist',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

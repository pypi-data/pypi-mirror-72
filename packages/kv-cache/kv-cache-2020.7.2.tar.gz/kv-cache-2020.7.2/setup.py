import setuptools

setuptools.setup(
    name='kv-cache',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

import setuptools

setuptools.setup(
    name='writable-property',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

import setuptools

setuptools.setup(
    name='requests-retry-on-exceptions',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

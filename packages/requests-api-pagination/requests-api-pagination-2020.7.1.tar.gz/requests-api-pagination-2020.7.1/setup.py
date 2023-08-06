import setuptools

setuptools.setup(
    name='requests-api-pagination',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

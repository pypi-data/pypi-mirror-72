import setuptools

setuptools.setup(
    name='requests-etag-cache',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

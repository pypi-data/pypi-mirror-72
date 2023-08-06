import setuptools

setuptools.setup(
    name='tests42',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/tests42']
)

import setuptools

setuptools.setup(
    name='github-create',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/github-create']
)

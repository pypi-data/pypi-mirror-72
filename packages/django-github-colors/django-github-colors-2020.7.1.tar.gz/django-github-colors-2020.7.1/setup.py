import setuptools

setuptools.setup(
    name='django-github-colors',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

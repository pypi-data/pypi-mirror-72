import setuptools

setuptools.setup(
    name='django-embed-gist',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

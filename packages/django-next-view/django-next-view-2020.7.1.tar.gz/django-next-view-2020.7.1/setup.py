import setuptools

setuptools.setup(
    name='django-next-view',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

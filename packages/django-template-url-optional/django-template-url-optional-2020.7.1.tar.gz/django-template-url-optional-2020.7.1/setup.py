import setuptools

setuptools.setup(
    name='django-template-url-optional',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

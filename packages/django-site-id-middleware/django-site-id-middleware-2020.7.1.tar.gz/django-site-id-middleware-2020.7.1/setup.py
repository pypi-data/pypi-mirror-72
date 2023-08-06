import setuptools

setuptools.setup(
    name='django-site-id-middleware',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

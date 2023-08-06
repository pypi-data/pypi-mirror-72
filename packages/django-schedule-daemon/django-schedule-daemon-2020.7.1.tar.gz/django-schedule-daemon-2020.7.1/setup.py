import setuptools

setuptools.setup(
    name='django-schedule-daemon',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

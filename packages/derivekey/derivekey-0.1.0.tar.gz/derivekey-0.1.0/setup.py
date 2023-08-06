from setuptools import setup
setup(
    name = 'derivekey',
    version = '0.1.0',
    install_requires=['fastecdsa'],
    packages = ['derivekey'],
    entry_points = {
        'console_scripts': [
            'derivekey = derivekey.__main__:main'
        ]
    })

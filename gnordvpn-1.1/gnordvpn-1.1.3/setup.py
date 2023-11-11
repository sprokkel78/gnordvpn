from setuptools import setup

setup(
    name='gnordvpn',
    version='1.1.2',
    packages=['gnordvpn'],
    install_requires=[
        'PyGObject',  # Add any dependencies here
    ],
    entry_points={
        'console_scripts': [
            'myapp = gnordvpn.py',  # Replace with your main script
        ],
    },
)





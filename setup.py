from setuptools import setup, find_packages
setup(
    name="IvideonLamp",
    version="0.1",
    packages=find_packages(),

    install_requires=['tornado==4.2.1'],

    author="Mikhail Vostrykh",
    author_email="mor.entharia@gmail.com",

    classifiers=[
        'Development Status :: 0 - Alfa',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)

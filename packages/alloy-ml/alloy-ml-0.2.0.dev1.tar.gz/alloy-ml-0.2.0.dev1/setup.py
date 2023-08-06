from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='alloy-ml',
    version='0.2.0.dev1',
    packages=['alloyml'],
    package_data={'alloyml': ['data/*']},
    url='https://github.com/marioboley/alloy-ml',
    license='MIT',
    author='Mario Boley',
    author_email='mario.boley@gmail.com',
    description='Machine learning methods for the prediction of alloy properties',
    long_description=long_description,
    python_requires='>=3.6',
    install_requires=['pandas>=0.25.0', 'matplotlib>=3.0.1'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)

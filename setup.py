from setuptools import (find_packages,
                        setup)

setup(
    name='frml',
    version='0.1.0',
    author='Francois Nelles',
    author_email='FrancoisNelles@gmail.com',
    description='An open source financial risk management library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/FrancoisNelles/frml',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=[
        # Update project dependencies here
    ],
)

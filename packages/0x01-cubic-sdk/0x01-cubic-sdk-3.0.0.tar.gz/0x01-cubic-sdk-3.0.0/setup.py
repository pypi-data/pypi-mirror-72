from setuptools import setup

setup(
    name='0x01-cubic-sdk',
    version='3.0.0',
    author='Hypercube',
    author_email='hypercube@0x01.me',
    url='https://github.com/Smart-Hypercube/cubic-sdk',
    license='MIT',
    description='Cubic SDK',
    long_description='',
    long_description_content_type='text/markdown',
    packages=['cubic'],
    python_requires='>=3.7',
    install_requires=[
        'msgpack>=1.0',
        'requests>=2.21',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
    ],
)

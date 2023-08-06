import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("version", "r") as fh:
    version = fh.read()

setuptools.setup(
    python_requires='>=2.7',
    install_requires=[
        'dpkt',
        ],
    include_package_data=True,

    name='pcap-analysis',
    version=version,
    author='Tyler N. Thieding',
    author_email='python@thieding.com',
    maintainer='Tyler N. Thieding',
    maintainer_email='python@thieding.com',
    url='https://gitlab.com/TNThieding/pcap-analysis',
    description='Analyze packet capture format (pcap) files.',
    long_description=long_description,
    download_url='https://gitlab.com/TNThieding/pcap-analysis',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Networking',
        ],
    license='MIT License',
    package_dir={"": "src"},
    packages=setuptools.find_packages('src')
)

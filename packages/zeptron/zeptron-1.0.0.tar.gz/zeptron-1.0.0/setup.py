import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f: 
    requirements = f.readlines() 

setuptools.setup(
    name="zeptron", # Replace with your own username
    version="1.0.0",
    author="Jose Mathias",
    author_email="hello@zeptron.co",
    description="A super lightweight streaming module using ZMQ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeptron/zeptron",
    packages=setuptools.find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'zeptron = script.zeptron:main'
            ]
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = requirements,
    python_requires='>=3.6',
)
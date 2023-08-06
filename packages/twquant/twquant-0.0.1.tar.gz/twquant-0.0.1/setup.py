import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'twquant',         
    version = '0.0.1',      
    description = 'retrieve financial-related data and use the data on investment decision making', 
    author = 'Gary',                   
    author_email = 'sarcas0705@gmail.com',      
    license="MIT", 
    long_description=long_description,
    long_description_content_type="text/markdown",  
    url = 'https://github.com/gary136/twquant',   

    # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    

    packages=setuptools.find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   
)

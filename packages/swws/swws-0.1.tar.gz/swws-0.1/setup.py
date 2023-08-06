from setuptools import setup


setup(
    name='swws',
    version='0.1',                          
    description='Package Description',                    
    install_requires=['discord'],
    packages=['swws'],
    author="SALAD37",
    author_email="nonemovo@gmail.com",
    project_urls={
        "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://code.example.com/HelloWorld/",
    },
    long_description_content_type = 'text/markdown',
    long_description = open('README.md', 'r+').read()
) 
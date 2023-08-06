import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="driveways-project-cis4930-v6", # Replace with your own username
    version="0.0.8",
    author="Andres Canas, Henry Parker, Dylan Fay, Zack Saadioui",
    description="Driveways Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henryparker/drivewaynew",
    packages=['drive','userface','sample_app',],
    py_modules=["manage"],
    include_package_data = True,
    install_requires = ['asgiref', 'astroid', 'certifi', 'chardet', 'Django', 'django-crispy-forms', 'django-leaflet', 'geographiclib', 'geopy', 'idna', 'isort', 'lazy-object-proxy==1.4.*', 'mccabe', 'psycopg2-binary', 'pylint', 'pytz', 'requests', 'six', 'sqlparse', 'toml', 'typed-ast', 'urllib3', 'wrapt'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    
    entry_points =

    { 'console_scripts':

        [

            'runmyserver = sample_app.run:main',


        ]

    },
)
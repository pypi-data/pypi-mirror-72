
# Labs CDK!

This project is used to define aws cdk constructs which can be used by labs as building 
blocks for creating applications.

### Set up
Install python3
```
$ brew install python3
```

Create a virtualenv.

```
$ pip install virtualenvwrapper
$ mkvirtualenv labs-cdk --python=python3
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
$ pip install twine
```

Install nodejs from https://nodejs.org/en/download/

Install aws cdk npm package

```
$ npm install
```


### Build and upload to PyPI
Update the version number in setup.py

Build the package
```
$ python setup.py sdist bdist_wheel
```

Deploy to PyPi
```
$ twine upload -r pypi dist/labs_cdk-{version-number}*
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

#!/bin/bash
# exit when any command fails
set -o errexit
set -x

cd ..
rm -rf my_awesome_project

# install test requirements
pip install -r fastapi-cookiecutter/requirements/dev.txt

# create the project using the default settings in cookiecutter.json
PYV=`python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`
cookiecutter fastapi-cookiecutter --no-input python_version=$PYV
cd my_awesome_project

# run tests first, because it will install all the requirements.
make test

# test docs building
cd docs
make html
cd ../

# test service running
python my_awesome_project/main.py &
sleep 20

expected_version="{\"version\":\"0.1.0\"}"
actual_version=`curl http://localhost:8080/api/v1/version`

if [ "$expected_version" != "$actual_version" ]
then
    echo "Not equal"
    exit 1
fi

# clean up the generated folders
cd ..
rm -r my_awesome_project
cd fastapi-cookiecutter/
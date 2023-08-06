#!/usr/bin/env bash
python setup.py sdist
python setup.py bdist_wheel
python setup.py bdist_egg
twine check dist/*
#python setup.py sdist upload
twine upload --skip-existing dist/*whl dist/*gz dist/*egg

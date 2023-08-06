#!/bin/bash
# run tests and keep watching them
# I need a separate test runner as WingIde6.1 will fails when we pass coverage arguments
# so I modified run_pytest_xml.py runner to do not pass []'-p', 'no:terminal']
# so I can still run test from IDE
# but using ths script is possible to run in a CI fashion
# all tests, coverage, etc.

# n=auto
pytest -f --durations=5 --color=yes --cov=brotation --cov-append --cov-report html --maxfail=5 $@

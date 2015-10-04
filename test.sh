#!/usr/bin/env bash
# Exit upon first failure
set -e

# Allow for skipping lint during development
if test "$SKIP_LINT" != "TRUE"; then
  flake8 *.py suplemon/
fi

# Run our tests
# python setup.py nosetests

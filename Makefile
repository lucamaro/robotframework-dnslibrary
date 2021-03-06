# This file is part of robotframework-dnslibrary.
# https://github.com/lucamaro/robotframework-dnslibrary

# Licensed under the Apache License 2.0 license:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2016, Luca Maragnani <luca.maragnani@gmail.com>


# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

# install
setup:
	@python setup.py install

# test your application (tests in the tests/ directory)
test: unit e2e

unit:
	@nosetests --with-coverage --cover-erase --cover-html --cover-package DNSLibrary #--cover-min-percentage=80

e2e:
	@pybot -d tmp/ tests/e2e.txt

# run tests against all supported python versions
tox:
	@tox

docs:
	@python -m robot.libdoc DNSLibrary docs/index.html

clean:
	@rm -rf build/ dist/ tmp/ cover/ robotframework_dnslibrary.egg-info

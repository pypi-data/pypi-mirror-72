build:
	/usr/bin/python setup.py bdist_wheel
install:
	/usr/bin/env pip install -e .[dev]
sdist:
	/usr/bin/env python setup.py sdist
publish: build sdist
	twine upload dist/*
uninstall:
	/usr/bin/env pip uninstall -y greetuvm
rm:
	rm -rf {archived,latest}_logs build dist src/*.egg-info
clean: uninstall rm


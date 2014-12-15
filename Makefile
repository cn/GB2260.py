PYTHON := python
PYTEST := py.test
TOX := tox

.PHONY: all build test test-all clean

all: build

build: gb2260/data.py
	$(PYTHON) setup.py sdist bdist_wheel

test: gb2260/data.py
	$(PYTEST)

test-all: gb2260/data.py
	$(TOX)

clean:
	rm -rf dist build gb2260/data.py

gb2260/data.py: data/GB2260*.txt
	$(PYTHON) generate.py $? $@

data/GB2260*.txt:
	git submodule init
	git submodule update

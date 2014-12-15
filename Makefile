PYTHON := python

.PHONY: all build clean

all: build

build: gb2260/data.py
	$(PYTHON) setup.py sdist bdist_wheel

clean:
	rm -rf dist build gb2260/data.py

gb2260/data.py: data/GB2260*.txt
	$(PYTHON) generate.py $? $@

data/GB2260*.txt:
	git submodule init
	git submodule update

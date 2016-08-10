SHELL := $(shell echo $$SHELL)

.PHONY: install
install: 
	echo export ssf2conll="$(CURDIR)" >> ~/.bashrc
	source ~/.bashrc

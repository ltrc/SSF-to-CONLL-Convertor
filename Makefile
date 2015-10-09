SHELL := $(shell echo $$SHELL)
install: 
	echo export ssf2conll="$(CURDIR)" >> ~/.bashrc
	source ~/.bashrc

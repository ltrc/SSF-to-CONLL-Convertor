#
# Makefile -- compiling/copying/install/uninstall the module
#

PREFIX = $(setu)

# Program and Data files and directories.
DEST_PROG_DIR = $(PREFIX)/src/sl/headcomputation-
VER = 1.8
CPFR = cp -fr

# make all -- make programs, library, documentation, etc.

all:install-src 

install-src:
	mkdir -p $(DEST_PROG_DIR)$(VER)
	cp -fr src tests README-usr README-dev INSTALL headcomputation.pl doc API ChangeLog $(DEST_PROG_DIR)$(VER)
	$(CPFR) headcomputation_run.sh headcomputation.sh headcomputation.spec $(DEST_PROG_DIR)$(VER)
	cp Makefile.stage2 $(DEST_PROG_DIR)$(VER)/Makefile

# make compile -- Compiles the source code
# compile: compile-exec

# make install -- Install what all needs to be installed, copying the files from the packages tree to systemwide directories.# it installs the engine and the corpus, dictionary, etc.


# remove the module files from sampark
clean:uninstall
uninstall:
	$(MAKE) -C  $(DEST_PROG_DIR)$(VER) clean
	rm -fr $(DEST_PROG_DIR)$(VER) 

.PHONY: all clean install uninstall install-src 


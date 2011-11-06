
BASE=$(DESTDIR)/opt/aquilon

build:

install:
	-mkdir -p $(BASE)/lib
	rsync -av pylons/ $(BASE)/lib/pylons
	-mkdir -p $(BASE)/etc/sv
	rsync -av etc/pylons/ $(BASE)/etc/sv/pylons

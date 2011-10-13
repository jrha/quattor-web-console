
BASE=/opt/aquilon

install:
	rsync -av pylons/ $(BASE)/lib/pylons
	mkdir $(BASE)/etc/sv
	rsync -av etc/pylons/ $(BASE)/etc/sv/pylons

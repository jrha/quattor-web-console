
BASE=$(DESTDIR)/opt/aquilon

build:

install:
	rsync -av opt $(DESTDIR)/
	chown -R cdb $(DESTDIR)
	rsync -av var $(DESTDIR)/
	chown -R cdb $(DESTDIR)/var/lib/supervise/*
	install -m 0644 -o cdb -D opt/aquilon/etc/appliance.conf $(DESTDIR)/etc/aqd.conf

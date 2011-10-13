
DESTDIR=/opt/aquilon/lib/pylons


install:
	rsync -av pylons/ $(DESTDIR)

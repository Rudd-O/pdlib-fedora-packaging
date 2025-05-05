# pdlib packaging for Fedora

Upstream pdlib packageable by you.

Get source:

```bash
# requires rpmspec to be installed
src=$(rpmspec -P pdlib.spec | grep Source | awk ' { print $2 } ')
# requires wget to be installed
wget "$src"
# requires mock to be installed
# replace fedora-41-x86_64 with anything under /etc/mock
mock -r fedora-41-x86_64 --buildsrpm --spec pdlib.spec --sources ./ --resultdir=out
mock -r fedora-41-x86_64 --rebuild out/pdlib*src.rpm --resultdir=out
```

Find your built RPMs in the `out` directory.

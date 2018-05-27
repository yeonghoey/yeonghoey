SHELL = /bin/bash

PANDOC = pandoc
DESTDIR = docs

# content
content_src = content/%/README.org
content_dst = $(DESTDIR)/%/index.html

content_src_files = $(wildcard $(subst %,**,$(content_src)))
content_dst_files = \
	$(patsubst $(content_src),$(content_dst),$(content_src_files))

# static
static_src = static/%
static_dst = $(DESTDIR)/%
static_src_files = $(wildcard $(subst %,**,$(static_src)))
static_dst_files = \
	$(patsubst $(static_src),$(static_dst),$(static_src_files))


.PHONY: all dev clean

all: $(content_dst_files) $(static_dst_files)

dev:
	pipenv run python scripts/dev.py

clean:
	-rm -rf $(DESTDIR)

$(content_dst) : $(content_src)
	mkdir -p "$(dir $@)"
	$(PANDOC) '$<' --mathjax -s -o '$@'

$(static_dst) : $(static_src)
	cp '$<' '$@'

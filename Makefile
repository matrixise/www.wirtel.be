USERID:=$(shell id -u)
GROUPID:=$(shell id -g)

-include .env

build-cv:
	docker run --rm --user=$(USERID):$(GROUPID) -v $(PWD):/src/ -w /src/ aergus/latex pdflatex StephaneWirtel.tex

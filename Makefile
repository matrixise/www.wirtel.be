USERID:=$(shell id -u)
GROUPID:=$(shell id -g)

-include .env
# --user=$(USERID):$(GROUPID) \

build-html:
	docker run --rm \
		-e HUGO_DESTINATION=/public \
		-e HUGO_THEME=ghostwriter \
		-v $(PWD):/src/ \
		-v /tmp/hugo-build-output:/public \
		jojomi/hugo

build-cv:
	docker run --rm --user=$(USERID):$(GROUPID) \
		-v $(PWD):/src/ \
		-w /src/ aergus/latex \
		pdflatex StephaneWirtel.tex

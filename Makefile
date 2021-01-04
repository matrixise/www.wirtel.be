USERID:=$(shell id -u)
GROUPID:=$(shell id -g)
BUILD_DIR=/tmp/hugo-build-output
-include .env
# --user=$(USERID):$(GROUPID) \

build-html:
	docker run --rm \
		-e HUGO_DESTINATION=/public \
		-e HUGO_THEME=ghostwriter \
		-v $(PWD):/src/ \
		-v $(BUILD_DIR):/public \
		jojomi/hugo

build-cv:
	docker run --rm --user=$(USERID):$(GROUPID) \
		-v $(PWD):/src/ \
		-w /src/ aergus/latex \
		pdflatex StephaneWirtel.tex

run:
	docker run --rm \
		-e HUGO_DESTINATION=/public \
		-e HUGO_THEME=ghostwriter \
		-v $(PWD):/src/ \
		-v $(BUILD_DIR):/public \
		--publish-all \
		jojomi/hugo \
		hugo server --bind=0.0.0.0

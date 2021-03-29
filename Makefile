USERID:=$(shell id -u)
GROUPID:=$(shell id -g)
BUILD_DIR=/tmp/hugo-build-output
DOCKER_IMAGE=jojomi/hugo:0.65

-include .env

install_dependencies:
	pip install -r scripts/requirements.txt

update_dependencies:
	pip freeze | sort > scripts/requirements.txt

update-submodules:
	git submodule update --init --recursive

generate-cv:
	python scripts/generate-cv.py templates/TemplateCV.tex StephaneWirtel.tex

build-html: update-submodules
	docker run --rm \
		-e HUGO_DESTINATION=/public \
		-e HUGO_THEME=ghostwriter \
		-v $(PWD):/src/ \
		-v $(BUILD_DIR):/public \
		$(DOCKER_IMAGE)

build-cv:
	docker run --rm --user=$(USERID):$(GROUPID) \
		-v $(PWD):/src/ \
		-w /src/ aergus/latex \
		make make_pdf

make_pdf:
	pdflatex StephaneWirtel.tex

run: update-submodules
	docker run --rm \
		-e HUGO_DESTINATION=/public \
		-e HUGO_THEME=ghostwriter \
		-v $(PWD):/src/ \
		-v $(BUILD_DIR):/public \
		--publish 1313:1313 \
		$(DOCKER_IMAGE) \
		hugo server --bind=0.0.0.0

build: generate-cv build-cv build-cv

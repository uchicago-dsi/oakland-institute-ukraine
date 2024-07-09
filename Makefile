mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
current_abs_path := $(subst Makefile,,$(mkfile_path))
ARCH := $(shell uname -m)

include .env

paths:
	@echo $(mkfile_path)
	@echo $(current_dir)
	@echo $(current_abs_path)

build:
	cd $(current_abs_path)
	docker build . -t oi-ukraine --build-arg ARCH=$(ARCH)

run-pipeline:
	cd $(current_abs_path)
	docker run -u 1000:1000 -e COUNTRY=$(COUNTRY) -v $(current_abs_path):/app -t oi-ukraine

jupyter:
	cd $(current_abs_path)
	docker run -v $(current_abs_path):/app --rm -p 8888:8888 -t oi-ukraine jupyter lab --port=8888 --ip='*' --NotebookApp.token='' --NotebookApp.password='' --no-browser --notebook-dir=/app/notebooks --allow-root

bash:
	cd $(current_abs_path)
	docker run -v $(current_abs_path):/app -it -t oi-ukraine /bin/bash

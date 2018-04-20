.PHONY: run debug build size version

VOLUMES=\
-v /etc:/host/etc:ro \
-v /run:/host/run:ro \
-v /sys:/host/sys:ro \
-v /usr:/host/usr:ro \
-v /var:/host/var:rw

build:
	docker build -t container-check .

run:
	docker run ${VOLUMES} \
	-it --privileged --rm --name container-check container-check

debug:
	docker run ${VOLUMES} \
	-it --privileged --rm --name container-check container-check ./container_check --debug

test:
	docker run ${VOLUMES} \
	-it --privileged --rm --name container-check container-check ./checking/unittest_coverage.py

version:
	docker run \
	-it --privileged --rm --name container-check container-check ./container_check --version

help: build
	docker run \
	-it --privileged --rm --name container-check container-check ./container_check --help

size:
	@docker image list container-check --format 'Current Size: {{.Repository}} {{.Size}}\n'

clean: size
	find . -type f -name '*.pyc' -exec rm '{}' ';' ||:
	docker ps --all --filter 'status=exited' --format '{{.ID}}' | xargs docker rm ||:
	docker image list --filter 'dangling=true' --format '{{.ID}}' | xargs docker rmi ||:

.PHONY: run debug build size version

build:
	docker build -t container-check .

run:
	docker run \
	-v /etc:/host/etc:ro \
	-v /run:/host/run:ro \
	-v /sys:/host/sys:ro \
	-v /usr:/host/usr:ro \
	-v /var:/host/var:ro \
	-it --privileged --rm --name container-check container-check

debug:
	docker run \
	-v /etc:/host/etc:ro \
	-v /run:/host/run:ro \
	-v /sys:/host/sys:ro \
	-v /usr:/host/usr:ro \
	-v /var:/host/var:ro \
	-it --privileged --rm --name container-check container-check ./container-check --debug

version:
	docker run \
	-it --privileged --rm --name container-check container-check ./container-check --version

size:
	@docker image list container-check --format 'Current Size: {{.Repository}} {{.Size}}\n'

clean: size
	find . -type f -name '*.pyc' -exec rm '{}' ';' ||:
	docker ps --all --filter 'status=exited' --format '{{.ID}}' | xargs docker rm ||:
	docker image list --filter 'dangling=true' --format '{{.ID}}' | xargs docker rmi ||:

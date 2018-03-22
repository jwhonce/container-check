.PHONY: run debug build

run:
	docker run \
	-v /etc:/host/etc:ro \
	-v /usr:/host/usr:ro \
	-v /var:/host/var:ro \
	-it --privileged --rm --name container-check container-check

debug:
		docker run \
		-v /etc:/host/etc:ro \
		-v /usr:/host/usr:ro \
		-v /var:/host/var:ro \
		-it --privileged --rm --name container-check container-check ./container-check --debug

build:
	docker build -t container-check .

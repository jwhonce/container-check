.PHONY: run debug build

run:
	docker run \
	-v /etc:/host/etc:ro \
	-v /usr:/host/usr:ro \
	-v /var:/host/var:ro \
	-v /run:/host/run:ro \
	-v /sys:/host/sys:ro \
	-it --privileged --rm --name container-check container-check

debug:
		docker run \
		-v /etc:/host/etc:ro \
		-v /usr:/host/usr:ro \
		-v /var:/host/var:ro \
		-v /sys:/host/sys:ro \
		-it --privileged --rm --name container-check container-check ./container-check --debug

build:
	docker build -t container-check .


clean:
	find . -type f -name '*.pyc' -exec rm '{}' ';' ||:
	docker ps --all --filter 'status=exited' --format '{{.ID}}' | xargs docker rm ||:
	docker image list --filter 'dangling=true' --format '{{.ID}}' | xargs docker rmi ||:

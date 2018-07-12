.PHONY: run debug build size version

VOLUMES=\
-v /boot:/host/boot:ro \
-v /etc:/host/etc:ro \
-v /proc:/host/proc:ro \
-v /run:/host/run:ro \
-v /sys:/host/sys:ro \
-v /usr:/host/usr:ro \
-v /var:/host/var:ro

OPTIONS=\
-it \
--privileged \
--rm \
--cap-add=NET_ADMIN \
--net=host \
--name container-check \
container-check

build:
	docker build -t container-check .

run:
	docker run ${VOLUMES} \
	${OPTIONS} ./container_check --checks=./cis_checks
	#-it --privileged --rm --name container-check container-check ./container_check --checks=./cis_checks:./checks

shell:
	docker run ${VOLUMES} \
	${OPTIONS} /bin/bash -i

debug:
	docker run ${VOLUMES} \
	${OPTIONS} ./container_check --debug

test:
	docker run ${VOLUMES} \
	${OPTIONS} ./checking/unittest_coverage.py

version:
	docker run \
	${OPTIONS} ./container_check --version

help: build
	docker run \
	${OPTIONS} ./container_check --help

size:
	@docker image list container-check --format 'Current Size: {{.Repository}} {{.Size}}\n'

clean: size
	find . -type f -name '*.pyc' -exec rm '{}' ';' ||:
	docker ps --all --filter 'status=exited' --format '{{.ID}}' | xargs docker rm ||:
	docker image list --filter 'dangling=true' --format '{{.ID}}' | xargs docker rmi ||:

FROM centos:7

WORKDIR /usr/src/app

LABEL \
        License="Apache-2.0"

ENV PKG_LIST \
    audit-libs-python \
    container-selinux \
    dbus-python \
    libselinux-python \
    python2-mock \
    python2-pip \
    systemd-python \
    mt-st

RUN \
    yum install --setopt=tsflags=nodocs -y epel-release && \
    yum install --setopt=tsflags=nodocs -y ${PKG_LIST} && \
    rpm -V ${PKG_LIST} && \
    yum clean all && \
    rm -rf /var/cache/yum

COPY . .

RUN \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/pip/

CMD [ "python", "./container_check" ]

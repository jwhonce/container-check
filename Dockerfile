FROM centos:7

WORKDIR /usr/src/app

LABEL \
        License="Apache-2.0"

ENV PKG_LIST \
    audit-libs-python \
    augeas \
    container-selinux \
    dbus-python \
    iptables \
    libselinux-python \
    mt-st \
    python-augeas \
    python2-mock \
    python2-pip \
    systemd-python

RUN \
    yum install --setopt=tsflags=nodocs -y epel-release && \
    yum install --verbose --setopt=tsflags=nodocs -y ${PKG_LIST} && \
    rpm -V ${PKG_LIST} && \
    yum clean all && \
    rm -rf /var/cache/yum

COPY . .

RUN \
    pip install --no-cache-dir -r requirements.txt && \
    cp ntp.aug /usr/share/augeas/lenses/dist/ntp.aug && \
    cp systemd.aug /usr/share/augeas/lenses/dist/systemd.aug && \
    rm -rf ~/.cache/pip/

CMD [ "python", "./container_check" ]

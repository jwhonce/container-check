FROM centos:7

WORKDIR /usr/src/app

LABEL \
        License="Apache-2.0"

ENV PKG_LIST container-selinux python2-pip libselinux-python

RUN \
    yum install --setopt=tsflags=nodocs -y epel-release && \
    yum install --setopt=tsflags=nodocs -y ${PKG_LIST} && \
    rpm -V ${PKG_LIST} && \
    yum clean all

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./container-check" ]

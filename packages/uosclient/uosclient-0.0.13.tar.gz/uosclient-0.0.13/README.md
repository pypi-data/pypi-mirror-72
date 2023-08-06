Unipart OpenStack client tools
==============================

[![Build Status](https://travis-ci.com/unipartdigital/uosclient.svg?branch=master)](https://travis-ci.com/unipartdigital/uosclient)

This is a set of simple tools designed to automate various common
system administration tasks within the Unipart OpenStack
infrastructure.

These tools are highly opinionated and inflexible by design, since the
purpose is to ensure consistency in the way that system administration
tasks are performed.

Installation
------------

### Fedora / CentOS 8

```shell
dnf copr enable unipartdigital/pkgs
dnf install uosclient
```

### CentOS 7

```shell
yum-config-manager --add-repo \
     https://copr.fedorainfracloud.org/coprs/unipartdigital/pkgs/repo/epel-7/unipartdigital-pkgs-epel-7.repo
yum install uosclient
```

### Other

```shell
pip3 install uosclient
```

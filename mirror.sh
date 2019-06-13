#!/usr/bin/env bash
set -ex

# 换源
# 不用在服务器执行这个脚本
cp /var/www/belife/misc/sources.list /etc/apt/sources.list
mkdir -p /root/.pip
cp /var/www/belife/misc/pip.conf /root/.pip/pip.conf
apt-get update
#!/bin/bash 
proxyaddr=118.103.111.152:8080
export https_proxy=$proxyaddr
export http_proxy=$proxyaddr
wget -c $1

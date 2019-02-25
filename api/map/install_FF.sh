#!/usr/bin/sh

sudo apt-get install flex bison

wget https://fai.cs.uni-saarland.de/hoffmann/ff/FF-v2.3-big-parse-suda.tgz
tar xvzf FF-v2.3-big-parse-suda.tgz

cd FF-v2.3-big-parse-suda
make

cp ff ~

rm -fr FF-*
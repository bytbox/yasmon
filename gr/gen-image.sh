#!/bin/sh

#get to the right directory
dn=`dirname $0`
cd $dn

OPTS="-background transparent"

for x in 16 22 24 32 36 48 64 72 96 128 192 256
do
    echo -n "Generating ${x}x${x}... "
    mkdir -p ${x}x${x}
    convert $OPTS -resize ${x}x${x} yasmon.svg ${x}x${x}/yasmon.png
    echo done!
done

#default is 64x64
cp yasmon-64.png yasmon.png

#!/bin/sh

#check to make sure we have convert
if test ! -x /usr/bin/convert
then
    echo "$0: error: convert not found (is imagemagick installed?)"
    exit 1
fi

#get to the right directory
dn=`dirname $0`
cd $dn

#options with which convert is called
OPTS="-background transparent"

#for each resolution
for x in 16 22 24 32 36 48 64 72 96 128 192 256
do
    if test ! -d ${x}x${x}
    then
	echo -n "Generating ${x}x${x}... "
	mkdir ${x}x${x}
	convert $OPTS -resize ${x}x${x} yasmon.svg ${x}x${x}/yasmon.png
	echo done!
    fi
done

#default is 64x64
cp 64x64/yasmon.png yasmon.png

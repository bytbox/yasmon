#!/bin/sh

#get to the right directory
dn=`dirname $0`
cd $dn

OPTS="-background transparent"

#create 16x16,24x24,32x32,48x48,64x64,128x128
convert $OPTS -resize 16x16   yasmon.svg yasmon-16.png
convert $OPTS -resize 24x24   yasmon.svg yasmon-24.png
convert $OPTS -resize 32x32   yasmon.svg yasmon-32.png
convert $OPTS -resize 48x48   yasmon.svg yasmon-48.png
convert $OPTS -resize 64x64   yasmon.svg yasmon-64.png
convert $OPTS -resize 128x128 yasmon.svg yasmon-128.png

#default is 64x64
cp yasmon-64.png yasmon.png

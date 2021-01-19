#!/bin/sh

rm -rf toLambdaFailerZip lambdaFailer.zip

mkdir toLambdaFailerZip

cp src/failer/*.py toLambdaFailerZip

cd toLambdaFailerZip

zip -r ../lambdaFailer.zip *

cd ..
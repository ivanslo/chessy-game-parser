#!/bin/sh
# write the code to create the lambda function.
# so far: all .py in src, and the `sly` folder of the virtual_env/lib/sly
rm -rf toLambdaParserPartialZip lambdaParserPartial.zip

mkdir toLambdaParserPartialZip

cp -R env/lib/python3.8/site-packages/sly toLambdaParserPartialZip
cp src/parser/*.py toLambdaParserPartialZip

cd toLambdaParserPartialZip
rm -rf __pycache__
rm -rf sly/__pycache__

zip -r ../lambdaParserPartial.zip *

cd ..

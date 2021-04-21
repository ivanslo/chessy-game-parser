#!/bin/sh
# write the code to create the lambda function.
# so far: all .py in src, and the `sly` folder of the virtual_env/lib/sly
rm -rf toLambdaParserZip lambdaParser.zip

mkdir toLambdaParserZip

cp -R env/lib/python3.8/site-packages/sly toLambdaParserZip
cp src/parser/*.py toLambdaParserZip

cd toLambdaParserZip
rm -rf __pycache__
rm -rf sly/__pycache__

zip -r ../lambdaParser.zip *

cd ..

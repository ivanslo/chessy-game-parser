#!/bin/sh
# write the code to create the lambda function.
# so far: all .py in src, and the `sly` folder of the virtual_env/lib/sly

rm -rf toZip lambda.zip

mkdir toZip

cp -R env/lib/python3.7/site-packages/sly toZip
cp src/*.py toZip

cd toZip
rm -rf __pycache__
rm -rf sly/__pycache__

zip -r ../lambda.zip *

cd ..
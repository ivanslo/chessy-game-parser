#!/bin/sh
FOLDER_LSZ=toLambdaSplitterZip
rm -rf $FOLDER_LSZ lambdaSplitter.zip

mkdir $FOLDER_LSZ

cp src/splitter/*.py $FOLDER_LSZ

cd $FOLDER_LSZ

rm -rf __pycache__

zip -r ../lambdaSplitter.zip *

cd ..
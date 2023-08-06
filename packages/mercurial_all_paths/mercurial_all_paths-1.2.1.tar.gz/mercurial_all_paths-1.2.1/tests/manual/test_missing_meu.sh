#!/bin/bash
#
# Verify what happens when meu is not installed, and when it is to be
# installed in emergency way.

DIR=`mktemp -d`
mkdir $DIR/inst
mkdir $DIR/hgrcpath

PIP=$DIR/venv/bin/pip
HG=$DIR/venv/bin/hg
export HGRCPATH=$DIR/hgrcpath

echo
echo "Preparation"
echo

python -m virtualenv --no-site-packages $DIR/venv

$PIP install Mercurial

cp ../../mercurial_all_paths.py $DIR/inst 

echo
echo "When it's missing (should fail reasonably)"
echo

$HG --config extensions.mercurial_all_paths=$DIR/inst/mercurial_all_paths.py \
     init $DIR/unimportant

echo
echo "When it's installed sideways (should work)"
echo

cp ../../../extension_utils/mercurial_extension_utils.py $DIR/inst

$HG --config extensions.mercurial_all_paths=$DIR/inst/mercurial_all_paths.py \
     init $DIR/unimportant2

echo
echo "When it's checked out sideways (should work)"
echo

$HG --config extensions.mercurial_all_paths=../../mercurial_all_paths.py \
     init $DIR/unimportant3


rm -rf $DIR

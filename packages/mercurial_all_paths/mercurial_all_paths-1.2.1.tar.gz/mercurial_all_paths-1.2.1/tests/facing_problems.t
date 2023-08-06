
Let's test behaviour when there are problems - some repo is missing,
another is unrelated.

Some locations used during testing:

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

  $ export BASE=$WORK_DIR/base
  $ export GOOD1=$WORK_DIR/good1
  $ export UNREL=$WORK_DIR/unrelated
  $ export MISSING=$WORK_DIR/missing
  $ export GOOD2=$WORK_DIR/good2

Some verifications, just to make sure

  $ mkdir -p $WORK_DIR
  $ cd $WORK_DIR
  $ pwd
  /tmp/cramtests-*/facing_problems.t/work (glob)

First we need appropriate Mercurial configuration file (and variable
which ensures it is used).

  $ export HGRCPATH=$WORK_DIR/hgrc
  $ mkdir -p $HGRCPATH

  $ cat > $HGRCPATH/basic.rc << EOF
  > [ui]
  > username = Andy Default <default@nowhere.net>
  > [extensions]
  > mercurial_all_paths =
  > EOF

We need some repositories to test.

  $ hg init "$BASE"
  $ hg init "$GOOD1"
  $ hg init "$UNREL"
  $ hg init "$GOOD2"

  $ cat > $BASE/.hg/hgrc << EOF
  > [paths]
  > good1=$GOOD1
  > unrel=$UNREL
  > missing=$MISSING
  > good2=$GOOD2
  > EOF

  $ cat > $UNREL/something.txt << EOF
  > This gonnna be unrelated.
  > EOF
  $ hg --cwd $UNREL add
  adding something.txt
  $ hg --cwd $UNREL commit -m "Unrelated"

Let's test pushing

  $ cat > $BASE/file.txt << EOF
  > Some text
  > EOF
  $ hg --cwd $BASE add
  adding file.txt
  $ hg --cwd $BASE commit -m 'First'

  $ hg --cwd $BASE pushall
  pushing to */good1 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  
  pushing to */unrelated (glob)
  searching for changes
  abort: repository is unrelated
  [255]

  $ hg --cwd $GOOD1 log --template '{rev}: {desc}\n'
  0: First

  $ hg --cwd $GOOD2 log --template '{rev}: {desc}\n'

  $ hg --cwd $UNREL log --template '{rev}: {desc}\n'
  0: Unrelated

and again, but in non-breaking mode

  $ cat >> $BASE/file.txt << EOF
  > More text
  > EOF
  $ hg --cwd $BASE commit -m 'Second'

This must go in quiet mode as various mercurials differ in the way they
report problems.

  $ hg --cwd $BASE pushall --ignore-errors --quiet
  error handling unrel: repository is unrelated
  error handling missing: repository .*/missing (does not exist|not found) (re)

  $ hg --cwd $GOOD1 log --template '{rev}: {desc}\n'
  1: Second
  0: First

  $ hg --cwd $GOOD2 log --template '{rev}: {desc}\n'
  1: Second
  0: First

  $ hg --cwd $UNREL log --template '{rev}: {desc}\n'
  0: Unrelated

Let's also test pulling 

  $ hg --cwd $GOOD1 update
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cat > $GOOD1/rep1.txt << EOF
  > Another text
  > EOF
  $ hg --cwd $GOOD1 add
  adding rep1.txt
  $ hg --cwd $GOOD1 commit -m "In repo1"

  $ hg --cwd $UNREL update
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cat > $UNREL/unr.txt << EOF
  > Another text
  > EOF
  $ hg --cwd $UNREL add
  adding unr.txt
  $ hg --cwd $UNREL commit -m "In unrel"

  $ hg --cwd $GOOD2 update
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cat > $GOOD2/rep1.txt << EOF
  > Another text
  > EOF
  $ hg --cwd $GOOD2 add
  adding rep1.txt
  $ hg --cwd $GOOD2 commit -m "In good2"

  $ hg --cwd $BASE incomingall
  comparing with */good1 (glob)
  searching for changes
  changeset:   2:* (glob)
  tag:         tip
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  
  comparing with */unrelated (glob)
  searching for changes
  abort: repository is unrelated
  [255]

  $ hg --cwd $BASE incomingall --ignore-errors
  comparing with */good1 (glob)
  searching for changes
  changeset:   2:* (glob)
  tag:         tip
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  
  comparing with */unrelated (glob)
  searching for changes
  error handling unrel: repository is unrelated
  
  error handling missing: repository */missing not found (glob)
  
  comparing with */good2 (glob)
  searching for changes
  changeset:   2:* (glob)
  tag:         tip
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In good2
  

  $ hg --cwd $BASE pullall  > $TMP/outp.txt
  abort: repository is unrelated
  [255]

  $ cat $TMP/outp.txt | grep -v '^new changesets'
  pulling from */good1 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)
  
  pulling from */unrelated (glob)
  searching for changes
 
  $ hg --cwd $BASE log --template '{rev}: {desc}\n'
  2: In repo1
  1: Second
  0: First

This also goes quiet due to differences between mercurials.

  $ hg --cwd $BASE pullall --ignore-errors --quiet
  error handling unrel: repository is unrelated
  error handling missing: repository */missing not found (glob)
 
  $ hg --cwd $BASE log --template '{rev}: {desc}\n'
  3: In good2
  2: In repo1
  1: Second
  0: First


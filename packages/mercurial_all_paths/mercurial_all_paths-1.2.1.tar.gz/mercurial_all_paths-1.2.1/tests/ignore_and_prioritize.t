
Let's test all_paths operations.

Some locations used during testing:

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

  $ export BASE=$WORK_DIR/base
  $ export REP1=$WORK_DIR/rep1
  $ export REP2=$WORK_DIR/rep2
  $ export REP3=$WORK_DIR/rep3

Some verifications, just to make sure

  $ mkdir -p $WORK_DIR
  $ cd $WORK_DIR
  $ pwd
  /tmp/cramtests-*/ignore_and_prioritize.t/work (glob)

First we need appropriate Mercurial configuration file (and variable
which ensures it is used).

  $ export HGRCPATH=$WORK_DIR/hgrc
  $ mkdir -p $HGRCPATH

  $ cat > $HGRCPATH/basic.rc << EOF
  > [ui]
  > username = Andy Default <default@nowhere.net>
  > [extensions]
  > mercurial_all_paths =
  > [all_paths]
  > ignore = unknown remote2
  > prioritize = remote3 mystery remote1
  > EOF

We need some repositories to test.

  $ hg init "$BASE"
  $ hg init "$REP1"
  $ hg init "$REP2"
  $ hg init "$REP3"

  $ cat > $BASE/.hg/hgrc << EOF
  > [paths]
  > remote1=$REP1
  > remote2=$REP2
  > remote3=$REP3
  > EOF

Let's test pushing

  $ cat > $BASE/file.txt << EOF
  > Some text
  > EOF

  $ hg --cwd $BASE add
  adding file.txt
  $ hg --cwd $BASE commit -m 'First'

  $ hg --cwd $BASE pushall
  pushing to */rep3 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  
  pushing to */rep1 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files

  $ hg --cwd $REP1 log --template '{rev}: {desc}\n'
  0: First

  $ hg --cwd $REP2 log --template '{rev}: {desc}\n'

  $ hg --cwd $REP3 log --template '{rev}: {desc}\n'
  0: First

Let's also test pulling 

  $ hg --cwd $REP1 update
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ cat > $REP1/rep1.txt << EOF
  > Another text
  > EOF

  $ hg --cwd $REP1 add
  adding rep1.txt
  $ hg --cwd $REP1 commit -m "In repo1"


  $ hg --cwd $REP2 update
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ cat >> $REP2/file.txt << EOF
  > From repo2…
  > EOF

  $ hg --cwd $REP2 add
  adding file.txt
  $ hg --cwd $REP2 commit -m "In repo2"

  $ hg --cwd $BASE incomingall
  comparing with */rep3 (glob)
  searching for changes
  no changes found
  comparing with */rep1 (glob)
  searching for changes
  changeset:   1:* (glob)
  tag:         tip
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  

  $ hg --cwd $BASE pullall    | grep -v '^new changesets '
  pulling from */rep3 (glob)
  searching for changes
  no changes found
  
  pulling from */rep1 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)

  $ hg --cwd $BASE log --template '{rev}: {desc}\n'
  1: In repo1
  0: First

  $ hg --cwd $BASE outgoingall
  comparing with */rep3 (glob)
  searching for changes
  changeset:   1:* (glob)
  tag:         tip
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  
  comparing with */rep1 (glob)
  searching for changes
  no changes found


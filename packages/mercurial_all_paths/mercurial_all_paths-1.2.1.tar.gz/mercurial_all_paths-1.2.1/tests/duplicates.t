
Let's test what happens when some paths aren't unique.

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
  /tmp/cramtests-*/duplicates.t/work (glob)

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
  $ hg init "$REP1"
  $ hg init "$REP2"
  $ hg init "$REP3"

  $ cat > $BASE/.hg/hgrc << EOF
  > [paths]
  > remote1=$REP1
  > remote2=$REP2
  > alias2=$REP2
  > alias1=$REP1
  > remote3=$REP3
  > alias1again=$REP1
  > EOF

Let's test pushing

  $ cat > $BASE/file.txt << EOF
  > Some text
  > EOF

  $ hg --cwd $BASE add
  adding file.txt
  $ hg --cwd $BASE commit -m 'First'

  $ hg --cwd $BASE pushall
  pushing to */rep1 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  
  pushing to */rep2 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  
  Skipping alias2 as path remote2 was already handled
  
  Skipping alias1 as path remote1 was already handled
  
  pushing to */rep3 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  
  Skipping alias1again as path remote1 was already handled

  $ hg --cwd $REP1 log --template '{rev}: {desc}\n'
  0: First

  $ hg --cwd $REP2 log --template '{rev}: {desc}\n'
  0: First

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
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ cat >> $REP2/file.txt << EOF
  > From repo2…
  > EOF

  $ hg --cwd $REP2 add
  $ hg --cwd $REP2 commit -m "In repo2"

  $ hg --cwd $BASE incomingall
  comparing with */rep1 (glob)
  searching for changes
  changeset:   1:* (glob)
  tag:         tip
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  
  comparing with */rep2 (glob)
  searching for changes
  changeset:   1:* (glob)
  tag:         tip
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo2
  
  Skipping alias2 as path remote2 was already handled
  
  Skipping alias1 as path remote1 was already handled
  
  comparing with */rep3 (glob)
  searching for changes
  no changes found
  Skipping alias1again as path remote1 was already handled

  $ hg --cwd $BASE pullall    | grep -v '^new changesets '
  pulling from */rep1 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)
  
  pulling from */rep2 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files (+1 heads)
  (run 'hg heads' to see heads, 'hg merge' to merge)
  
  Skipping alias2 as path remote2 was already handled
  
  Skipping alias1 as path remote1 was already handled
  
  pulling from */rep3 (glob)
  searching for changes
  no changes found
  
  Skipping alias1again as path remote1 was already handled

  $ hg --cwd $BASE log --template '{rev}: {desc}\n'
  2: In repo2
  1: In repo1
  0: First

  $ hg --cwd $BASE outgoingall
  comparing with */rep1 (glob)
  searching for changes
  changeset:   2:.* (re)
  tag:         tip
  parent:      0:.* (re)
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo2
  
  comparing with */rep2 (glob)
  searching for changes
  changeset:   1:* (glob)
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  
  Skipping alias2 as path remote2 was already handled
  
  Skipping alias1 as path remote1 was already handled
  
  comparing with */rep3 (glob)
  searching for changes
  changeset:   1:* (glob)
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  
  changeset:   2:* (glob)
  tag:         tip
  parent:      0:* (glob)
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo2
  
  Skipping alias1again as path remote1 was already handled

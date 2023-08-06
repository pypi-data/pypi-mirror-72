
Let's test group paths, configured with modern syntax.

Some locations used during testing:

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

  $ export BASE=$WORK_DIR/base
  $ export REP1=$WORK_DIR/rep1
  $ export REP2=$WORK_DIR/rep2
  $ export REP3=$WORK_DIR/rep3
  $ export REP4=$WORK_DIR/rep4

Some verifications, just to make sure

  $ mkdir -p $WORK_DIR
  $ cd $WORK_DIR
  $ pwd
  /tmp/cramtests-*/groups-modern.t/work (glob)

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
  > group.odd = remote1 remote3
  > group.even = remote2 remote4
  > EOF

We need some repositories to test.

  $ hg init "$BASE"
  $ hg init "$REP1"
  $ hg init "$REP2"
  $ hg init "$REP3"
  $ hg init "$REP4"

and configuration of groups:

  $ cat > $BASE/.hg/hgrc << EOF
  > [paths]
  > remote1=$REP1
  > remote2=$REP2
  > remote3=$REP3
  > remote4=$REP4
  > EOF

Let's test pushing

  $ cat > $BASE/file.txt << EOF
  > Some text
  > EOF

  $ hg --cwd $BASE add
  adding file.txt
  $ hg --cwd $BASE commit -m 'First'

  $ hg --cwd $BASE pushall -g odd
  pushing to */rep1 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  
  pushing to */rep3 (glob)
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

  $ hg --cwd $REP4 log --template '{rev}: {desc}\n'


  $ cat >> $BASE/file.txt << EOF
  > More text
  > EOF

  $ hg --cwd $BASE commit -m 'Second'


  $ hg --cwd $BASE pushall --group even
  pushing to */rep2 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 2 changesets with 2 changes to 1 files
  
  pushing to */rep4 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 2 changesets with 2 changes to 1 files

  $ hg --cwd $REP1 log --template '{rev}: {desc}\n'
  0: First

  $ hg --cwd $REP2 log --template '{rev}: {desc}\n'
  1: Second
  0: First

  $ hg --cwd $REP3 log --template '{rev}: {desc}\n'
  0: First

  $ hg --cwd $REP4 log --template '{rev}: {desc}\n'
  1: Second
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

  $ hg --cwd $REP2 commit -m "In repo2"

  $ hg --cwd $BASE incomingall --group odd
  comparing with */rep1 (glob)
  searching for changes
  changeset:   1:* (glob)
  tag:         tip
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  
  comparing with */rep3 (glob)
  searching for changes
  no changes found

  $ hg --cwd $BASE incomingall --group even
  comparing with */rep2 (glob)
  searching for changes
  changeset:   2:.* (re)
  tag:         tip
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo2
  
  comparing with */rep4 (glob)
  searching for changes
  no changes found

  $ hg --cwd $BASE pullall -g odd    | grep -v '^new changesets '
  pulling from */rep1 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files (+1 heads)
  (run 'hg heads' to see heads, 'hg merge' to merge)
  
  pulling from */rep3 (glob)
  searching for changes
  no changes found

  $ hg --cwd $BASE log --template '{rev}: {desc}\n'
  2: In repo1
  1: Second
  0: First

  $ hg --cwd $BASE outgoingall --group odd
  comparing with */rep1 (glob)
  searching for changes
  changeset:   1:* (glob)
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     Second
  
  comparing with */rep3 (glob)
  searching for changes
  changeset:   1:* (glob)
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     Second
  
  changeset:   2:* (glob)
  tag:         tip
  parent:      0:* (glob)
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  

  $ hg --cwd $BASE outgoingall --group even
  comparing with */rep2 (glob)
  searching for changes
  changeset:   2:* (glob)
  tag:         tip
  parent:      0:* (glob)
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  
  comparing with */rep4 (glob)
  searching for changes
  changeset:   2:* (glob)
  tag:         tip
  parent:      0:* (glob)
  user:        Andy Default <default@nowhere.net>
  date:        .* (re)
  summary:     In repo1
  

Wrong groups do not work

  $ hg --cwd $BASE pullall -g unknown
  abort: No paths defined in section unknown
  [255]

  $ hg --cwd $BASE incomingall --group unknown
  abort: No paths defined in section unknown
  [255]

  $ hg --cwd $BASE outgoingall --group unknown
  abort: No paths defined in section unknown
  [255]

  $ hg --cwd $BASE pushall -g unknown
  abort: No paths defined in section unknown
  [255]

But global access works

  $ hg --cwd $BASE pushall
  pushing to */rep1 (glob)
  searching for changes
  abort: push creates new remote head *! (glob)
  \((merge or see .hg help push. for details about pushing new heads|did you forget to merge.*)\) (re)
  [255]

  $ hg --cwd $BASE pullall    | grep -v '^new changesets '
  pulling from */rep1 (glob)
  searching for changes
  no changes found
  
  pulling from */rep2 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)
  
  pulling from */rep3 (glob)
  searching for changes
  no changes found
  
  pulling from */rep4 (glob)
  searching for changes
  no changes found

Finally let's test that push options work

  $ cat > $BASE/br1.txt << EOF
  > Br1 text
  > EOF

  $ hg --cwd $BASE branch br1
  marked working directory as branch br1
  (branches are permanent and global, did you want a bookmark?)
  $ hg --cwd $BASE add
  adding br1.txt
  $ hg --cwd $BASE commit -m 'Br1'

  $ cd $BASE
  $ pwd
  /tmp/cramtests-*/groups-modern.t/work/base (glob)
  $ hg update default 2>/dev/null   # --cwd $BASE
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ cat >> $BASE/file.txt << EOF
  > later text
  > EOF
  $ hg --cwd $BASE commit -m 'Normal'

  $ hg --cwd $BASE pushall -r default -f -g odd
  pushing to */rep1 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 3 changesets with 3 changes to 1 files (+1 heads)
  
  pushing to */rep3 (glob)
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 3 changesets with 3 changes to 1 files

  $ hg --cwd $BASE log --template '{rev}: {desc}\n'
  5: Normal
  4: Br1
  3: In repo2
  2: In repo1
  1: Second
  0: First

  $ hg --cwd $REP1 log --template '{rev}: {desc}\n'
  4: Normal
  3: In repo2
  2: Second
  1: In repo1
  0: First

  $ hg --cwd $REP2 log --template '{rev}: {desc}\n'
  2: In repo2
  1: Second
  0: First

  $ hg --cwd $REP3 log --template '{rev}: {desc}\n'
  3: Normal
  2: In repo2
  1: Second
  0: First


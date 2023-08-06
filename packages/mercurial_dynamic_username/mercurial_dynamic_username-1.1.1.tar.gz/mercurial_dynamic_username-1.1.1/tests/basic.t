
Let's test whether username is correct depending on the config.

Defining various locations:

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

  $ export TREE1=$WORK_DIR/tree1
  $ export TREE2="$WORK_DIR/tree 2"
  $ export TREE3="$WORK_DIR/tree3"
  $ export TREE4="$WORK_DIR/tree4"
  $ export REPO_1A=$TREE1/repo_a
  $ export REPO_1B=$TREE1/sub/repo_b
  $ export REPO_2A="$TREE2/repo_a"
  $ export REPO_2B="$TREE2/sub/repo_b"
  $ export REPO_3A=$TREE3/repo_a
  $ export REPO_3B=$TREE3/sub/repo_b
  $ export REPO_4A=$TREE4/repo_a
  $ export REPO_4B=$TREE4/sub/repo_b

First we need appropriate Mercurial configuration file (and variable
which ensures it is used).

  $ export HGRCPATH=$WORK_DIR/hgrc
  $ mkdir -p $HGRCPATH

  $ cat > $HGRCPATH/basic.rc << EOF
  > [ui]
  > username = Andy Default <default@nowhere.net>
  > [extensions]
  > mercurial_dynamic_username =
  > [dynamic_username]
  > work.location = $TREE1, "$TREE2"
  > work.username = Tim Worker <work@elsewhere.com>
  > hobby.location = $TREE4
  > hobby.username = Billy Hobbyist <hobby@inplace.org>
  > EOF

We need some repositories to test.

  $ hg init "$REPO_1A"
  $ hg init "$REPO_1B"
  $ hg init "$REPO_2A"
  $ hg init "$REPO_2B"
  $ hg init "$REPO_3A"
  $ hg init "$REPO_3B"
  $ hg init "$REPO_4A"
  $ hg init "$REPO_4B"

Time to test

  $ hg --cwd "$REPO_1A" showconfig ui.username
  Tim Worker <work@elsewhere.com>

  $ hg --cwd "$REPO_1B" showconfig ui.username
  Tim Worker <work@elsewhere.com>

  $ hg --cwd "$REPO_2A" showconfig ui.username
  Tim Worker <work@elsewhere.com>

  $ hg --cwd "$REPO_2B" showconfig ui.username
  Tim Worker <work@elsewhere.com>

  $ hg --cwd "$REPO_3A" showconfig ui.username
  Andy Default <default@nowhere.net>

  $ hg --cwd "$REPO_3B" showconfig ui.username
  Andy Default <default@nowhere.net>

  $ hg --cwd "$REPO_4A" showconfig ui.username
  Billy Hobbyist <hobby@inplace.org>

  $ hg --cwd "$REPO_4B" showconfig ui.username
  Billy Hobbyist <hobby@inplace.org>

Finally let's make some true commit

  $ cd "$REPO_4A"
  $ echo "X" > dummy.txt
  $ hg add dummy.txt
  $ hg commit -m "Dummy"
  $ hg log --template "{author}: {desc}\n"
  Billy Hobbyist <hobby@inplace.org>: Dummy

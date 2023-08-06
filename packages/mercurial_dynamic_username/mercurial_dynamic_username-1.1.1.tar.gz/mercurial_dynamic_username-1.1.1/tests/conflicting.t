
Test of longest dir picking and reverting to default.

Defining various locations:

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

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
  > top.location = $WORK_DIR
  > top.username = Tim Top <top@top.com>
  > topa.location = $WORK_DIR/a
  > ; No def
  > topab.location = $WORK_DIR/a/b $WORK_DIR/a/c
  > topab.username = Andy B <andyb@andyb.com>
  > EOF

We need some repositories to test.

  $ hg init $WORK_DIR/x
  $ hg init $WORK_DIR/a/x
  $ hg init $WORK_DIR/a/b/x
  $ hg init $WORK_DIR/a/c

Time to test

  $ hg --cwd $WORK_DIR/x showconfig ui.username
  Tim Top <top@top.com>
  $ hg --cwd $WORK_DIR/a/x showconfig ui.username
  Andy Default <default@nowhere.net>
  $ hg --cwd $WORK_DIR/a/b/x showconfig ui.username
  Andy B <andyb@andyb.com>
  $ hg --cwd $WORK_DIR/a/c showconfig ui.username
  Andy B <andyb@andyb.com>

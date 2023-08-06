
Basic path pattern operations test.

Defining various locations:

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

  $ export T1=$WORK_DIR/tree1
  $ export T2=$WORK_DIR/sub/tree2
  $ export T3=$WORK_DIR/tree3

... and custom Mercurial configuration files

  $ export HGRCPATH=$WORK_DIR/hgrc
  $ mkdir -p $HGRCPATH

  $ cat > $HGRCPATH/basic.rc << EOF
  > [ui]
  > username = Just Test <just.text@nowhere.com>
  > [extensions]
  > mercurial_path_pattern =
  > [path_pattern]
  > symm.local = $T1/{repo}
  > symm.remote = $T2/{repo}
  > flat.local = $T1/{repo}
  > flat.remote = $T3/{repo:/=-}
  > EOF

Let's create some repositories:

  $ mkdir -p $T1
  $ hg init $T1/repo_a
  $ hg init $T1/bbb/repo_b1
  $ hg init $T1/bbb/repo_b2
  $ hg init $T1/bbb/sub_b/repo_b3
  $ hg init $T1/bbb/sub_b/repo_b4

and two other trees:

  $ mkdir -p $T2
  $ mkdir -p $T3

as we test by local paths, we also need intermediate dirs:

  $ mkdir -p $T2/bbb/sub_b

and let's populate first tree a little bit:

  $ echo "X" > $T1/repo_a/x.txt
  $ hg --cwd $T1/repo_a add
  adding x.txt
  $ hg --cwd $T1/repo_a commit -m "First commit (X)"

  $ echo "Y" > $T1/bbb/repo_b1/y.txt
  $ hg --cwd $T1/bbb/repo_b1 add
  adding y.txt
  $ hg --cwd $T1/bbb/repo_b1 commit -m 'First commit ("Y")'

  $ echo "Z" > $T1/bbb/repo_b2/z.txt
  $ hg --cwd $T1/bbb/repo_b2 add
  adding z.txt
  $ hg --cwd $T1/bbb/repo_b2 commit -m 'First commit ("Z")'

  $ echo "A" > $T1/bbb/sub_b/repo_b3/a.txt
  $ hg --cwd $T1/bbb/sub_b/repo_b3 add
  adding a.txt
  $ hg --cwd $T1/bbb/sub_b/repo_b3 commit -m 'First commit ("A")'

  $ echo "B" > $T1/bbb/sub_b/repo_b4/b.txt
  $ hg --cwd $T1/bbb/sub_b/repo_b4 add
  adding b.txt
  $ hg --cwd $T1/bbb/sub_b/repo_b4 commit -m 'First commit ("B")'

Let's check paths:

  $ hg --cwd $T1/repo_a paths   | sort
  flat = /tmp/cramtests-*/basic.t/work/tree3/repo_a (glob)
  symm = /tmp/cramtests-*/basic.t/work/sub/tree2/repo_a (glob)

  $ hg --cwd $T1/bbb/repo_b1 paths    | sort
  flat = /tmp/cramtests-*/basic.t/work/tree3/bbb-repo_b1 (glob)
  symm = /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/repo_b1 (glob)

  $ hg --cwd $T1/bbb/repo_b2 paths    | sort
  flat = /tmp/cramtests-*/basic.t/work/tree3/bbb-repo_b2 (glob)
  symm = /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/repo_b2 (glob)

  $ hg --cwd $T1/bbb/sub_b/repo_b3 paths    | sort
  flat = /tmp/cramtests-*/basic.t/work/tree3/bbb-sub_b-repo_b3 (glob)
  symm = /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/sub_b/repo_b3 (glob)

  $ hg --cwd $T1/bbb/sub_b/repo_b4 paths    | sort
  flat = /tmp/cramtests-*/basic.t/work/tree3/bbb-sub_b-repo_b4 (glob)
  symm = /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/sub_b/repo_b4 (glob)

Then cloneto should actually create repositories:

  $ hg --cwd $T1/repo_a cloneto symm
  Cloning current repository to /tmp/cramtests-*/basic.t/work/sub/tree2/repo_a (resolved from: symm) (glob)
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ find $T2 -name .hg
  /tmp/cramtests-*/basic.t/work/sub/tree2/repo_a/.hg (glob)

  $ hg --cwd $T1/repo_a cloneto flat
  Cloning current repository to /tmp/cramtests-*/basic.t/work/tree3/repo_a (resolved from: flat) (glob)
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ find $T3 -name .hg
  /tmp/cramtests-*/basic.t/work/tree3/repo_a/.hg (glob)

  $ hg --cwd $T1/bbb/repo_b1 cloneto symm
  Cloning current repository to /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/repo_b1 (resolved from: symm) (glob)
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg --cwd $T1/bbb/repo_b1 cloneto flat
  Cloning current repository to /tmp/cramtests-*/basic.t/work/tree3/bbb-repo_b1 (resolved from: flat) (glob)
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ hg --cwd $T1/bbb/repo_b2 cloneto symm
  Cloning current repository to /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/repo_b2 (resolved from: symm) (glob)
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg --cwd $T1/bbb/repo_b2 cloneto flat
  Cloning current repository to /tmp/cramtests-*/basic.t/work/tree3/bbb-repo_b2 (resolved from: flat) (glob)
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ hg --cwd $T1/bbb/sub_b/repo_b3 cloneto symm
  Cloning current repository to /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/sub_b/repo_b3 (resolved from: symm) (glob)
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg --cwd $T1/bbb/sub_b/repo_b3 cloneto flat
  Cloning current repository to /tmp/cramtests-*/basic.t/work/tree3/bbb-sub_b-repo_b3 (resolved from: flat) (glob)
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ hg --cwd $T1/bbb/sub_b/repo_b4 cloneto symm
  Cloning current repository to /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/sub_b/repo_b4 (resolved from: symm) (glob)
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg --cwd $T1/bbb/sub_b/repo_b4 cloneto flat
  Cloning current repository to /tmp/cramtests-*/basic.t/work/tree3/bbb-sub_b-repo_b4 (resolved from: flat) (glob)
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ find $T2 -name .hg | sort
  /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/repo_b1/.hg (glob)
  /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/repo_b2/.hg (glob)
  /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/sub_b/repo_b3/.hg (glob)
  /tmp/cramtests-*/basic.t/work/sub/tree2/bbb/sub_b/repo_b4/.hg (glob)
  /tmp/cramtests-*/basic.t/work/sub/tree2/repo_a/.hg (glob)

  $ find $T3 -name .hg | sort
  /tmp/cramtests-*/basic.t/work/tree3/bbb-repo_b1/.hg (glob)
  /tmp/cramtests-*/basic.t/work/tree3/bbb-repo_b2/.hg (glob)
  /tmp/cramtests-*/basic.t/work/tree3/bbb-sub_b-repo_b3/.hg (glob)
  /tmp/cramtests-*/basic.t/work/tree3/bbb-sub_b-repo_b4/.hg (glob)
  /tmp/cramtests-*/basic.t/work/tree3/repo_a/.hg (glob)

Let's also check list_path_patterns:

  $ hg list_path_patterns
  Defined path patterns:
  flat
      local:  /tmp/cramtests-*/basic.t/work/tree1/{repo} (glob)
      remote: /tmp/cramtests-*/basic.t/work/tree3/{repo:/=-} (glob)
  symm
      local:  /tmp/cramtests-*/basic.t/work/tree1/{repo} (glob)
      remote: /tmp/cramtests-*/basic.t/work/sub/tree2/{repo} (glob)

Error reactions

  $ hg --cwd $T1/bbb/sub_b/repo_b3 cloneto niematakiegorepo
  abort: Unknown alias: niematakiegorepo\. Defined path aliases: (flat, symm|symm, flat) (re)
  [255]
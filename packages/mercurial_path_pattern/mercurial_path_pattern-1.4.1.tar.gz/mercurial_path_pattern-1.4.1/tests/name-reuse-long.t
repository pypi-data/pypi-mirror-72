
Reusing the same name for different patterns.

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

Custom Mercurial configuration file (including pattern defs)

  $ export HGRCPATH=$WORK_DIR/hgrc
  $ mkdir -p $HGRCPATH

  $ cat > $HGRCPATH/basic.rc << EOF
  > [ui]
  > username = Just Test <just.text@nowhere.com>
  > [extensions]
  > mercurial_path_pattern =
  > [path_pattern]
  > proda.local = $WORK_DIR/pylibs/{repo}
  > proda.remote = ssh://pydev@pyhost.com/{repo:/=-}
  > proda.alias = prod
  > prodb.local = $WORK_DIR/js/libs/{repo}
  > prodb.remote = https://johny@jshost.com/lib/{repo}
  > prodb.alias = prod
  > off1.local = $WORK_DIR/tracked/alah/beh
  > off1.remote = git+ssh://joe@github.com/alah-beh
  > off1.alias = official
  > off2.local = $WORK_DIR/tracked/something
  > off2.remote = https://bitbucket.com/messes
  > off2.alias = official
  > off3.local = $WORK_DIR/js/libs/xoxo
  > off3.remote = https://nodesse.js.com/xoxo
  > off3.alias = official
  > EOF

Creating some repos:

  $ hg init $WORK_DIR/pylibs/aaa/bbb
  $ hg init $WORK_DIR/pylibs/truncate
  $ hg init $WORK_DIR/js/libs/ander
  $ hg init $WORK_DIR/js/libs/var/sen
  $ hg init $WORK_DIR/js/libs/xoxo
  $ hg init $WORK_DIR/tracked/alah/beh
  $ hg init $WORK_DIR/tracked/belah/ah
  $ hg init $WORK_DIR/tracked/something
  $ hg init $WORK_DIR/tracked/something/else

Let's test effects:

  $ hg --cwd $WORK_DIR/pylibs/aaa/bbb paths
  prod = ssh://pydev@pyhost.com/aaa-bbb

  $ hg --cwd $WORK_DIR/pylibs/truncate paths
  prod = ssh://pydev@pyhost.com/truncate

  $ hg --cwd $WORK_DIR/js/libs/ander paths
  prod = https://johny@jshost.com/lib/ander

  $ hg --cwd $WORK_DIR/js/libs/var/sen paths
  prod = https://johny@jshost.com/lib/var/sen

  $ hg --cwd $WORK_DIR/js/libs/xoxo paths  | sort
  official = https://nodesse.js.com/xoxo
  prod = https://johny@jshost.com/lib/xoxo

  $ hg --cwd $WORK_DIR/tracked/alah/beh paths
  official = git+ssh://joe@github.com/alah-beh

  $ hg --cwd $WORK_DIR/tracked/belah/ah paths

  $ hg --cwd $WORK_DIR/tracked/something paths
  official = https://bitbucket.com/messes
 
  $ hg --cwd $WORK_DIR/tracked/something/else paths

And printed output:

  $ hg list_path_patterns
  Defined path patterns:
  official
      local:  /tmp/cramtests-*/name-reuse-long.t/work/tracked/alah/beh (glob)
      remote: git+ssh://joe@github.com/alah-beh
  official
      local:  /tmp/cramtests-*/name-reuse-long.t/work/tracked/something (glob)
      remote: https://bitbucket.com/messes
  official
      local:  /tmp/cramtests-*/name-reuse-long.t/work/js/libs/xoxo (glob)
      remote: https://nodesse.js.com/xoxo
  prod
      local:  /tmp/cramtests-*/name-reuse-long.t/work/pylibs/{repo} (glob)
      remote: ssh://pydev@pyhost.com/{repo:/=-}
  prod
      local:  /tmp/cramtests-*/name-reuse-long.t/work/js/libs/{repo} (glob)
      remote: https://johny@jshost.com/lib/{repo}


Reusing the same name for different patterns (short syntax).

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
  > prod.local = $WORK_DIR/pylibs/{repo}
  > prod.remote = ssh://pydev@pyhost.com/{repo:/=-}
  > prod.alt.local = $WORK_DIR/js/libs/{repo}
  > prod.alt.remote = https://johny@jshost.com/lib/{repo}
  > official.3.local = $WORK_DIR/js/libs/xoxo
  > official.1.local = $WORK_DIR/tracked/alah/beh
  > official.1.remote = git+ssh://joe@github.com/alah-beh
  > official.2.local = $WORK_DIR/tracked/something
  > official.2.remote = https://bitbucket.com/messes
  > official.3.remote = https://nodesse.js.com/xoxo
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

  $ hg --cwd $WORK_DIR/js/libs/xoxo paths   | sort
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
      local:  /tmp/cramtests-*/name-reuse-compact.t/work/tracked/alah/beh (glob)
      remote: git+ssh://joe@github.com/alah-beh
  official
      local:  /tmp/cramtests-*/name-reuse-compact.t/work/tracked/something (glob)
      remote: https://bitbucket.com/messes
  official
      local:  /tmp/cramtests-*/name-reuse-compact.t/work/js/libs/xoxo (glob)
      remote: https://nodesse.js.com/xoxo
  prod
      local:  /tmp/cramtests-*/name-reuse-compact.t/work/pylibs/{repo} (glob)
      remote: ssh://pydev@pyhost.com/{repo:/=-}
  prod
      local:  /tmp/cramtests-*/name-reuse-compact.t/work/js/libs/{repo} (glob)
      remote: https://johny@jshost.com/lib/{repo}

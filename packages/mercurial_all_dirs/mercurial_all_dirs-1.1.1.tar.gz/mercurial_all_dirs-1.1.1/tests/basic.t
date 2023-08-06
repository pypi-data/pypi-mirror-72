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
  > logtemplate = {author}: {desc} / {files}\n
  > [extensions]
  > mercurial_all_dirs =
  > EOF

Check help formatting:

  $ hg help alldirs | head -1
  hg alldirs ANY-MERCURIAL-COMMAND [COMMAND-ARGS]

Create some nested repositories:

  $ cd $WORK_DIR

  $ hg init aaa
  $ hg init bbb
  $ hg init ccc/one
  $ hg init ccc/two

And some files (so far manually to have different history):

  $ touch aaa/first.txt bbb/first.txt
  $ touch ccc/one/first.txt ccc/two/first.txt
  $ for d in aaa bbb ccc/one ccc/two; do hg --cwd $WORK_DIR/$d add; done
  adding first.txt
  adding first.txt
  adding first.txt
  adding first.txt
  $ for d in aaa bbb ccc/one ccc/two; do hg --cwd $WORK_DIR/$d commit -m "First file in $d"; done

Add and commit some files using alldirs:

  $ touch aaa/aaa.txt bbb/bbb.txt
  $ touch ccc/one/c-one.txt ccc/two/c-two.txt

  $ hg alldirs add
  => all_dirs: Executing add in /tmp/cramtests-*/basic.t/work/aaa (glob)
  adding aaa.txt
  => all_dirs: Executing add in /tmp/cramtests-*/basic.t/work/bbb (glob)
  adding bbb.txt
  => all_dirs: Executing add in /tmp/cramtests-*/basic.t/work/ccc/one (glob)
  adding c-one.txt
  => all_dirs: Executing add in /tmp/cramtests-*/basic.t/work/ccc/two (glob)
  adding c-two.txt

  $ hg alldirs commit -m "Second one"
  => all_dirs: Executing commit in /tmp/cramtests-*/basic.t/work/aaa (glob)
  => all_dirs: Executing commit in /tmp/cramtests-*/basic.t/work/bbb (glob)
  => all_dirs: Executing commit in /tmp/cramtests-*/basic.t/work/ccc/one (glob)
  => all_dirs: Executing commit in /tmp/cramtests-*/basic.t/work/ccc/two (glob)

Check history:

  $ hg alldirs log
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/aaa (glob)
  Andy Default <default@nowhere.net>: Second one / aaa.txt
  Andy Default <default@nowhere.net>: First file in aaa / first.txt
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/bbb (glob)
  Andy Default <default@nowhere.net>: Second one / bbb.txt
  Andy Default <default@nowhere.net>: First file in bbb / first.txt
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/ccc/one (glob)
  Andy Default <default@nowhere.net>: Second one / c-one.txt
  Andy Default <default@nowhere.net>: First file in ccc/one / first.txt
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/ccc/two (glob)
  Andy Default <default@nowhere.net>: Second one / c-two.txt
  Andy Default <default@nowhere.net>: First file in ccc/two / first.txt

Parametrized options:

  $ hg alld log -l 1 
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/aaa (glob)
  Andy Default <default@nowhere.net>: Second one / aaa.txt
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/bbb (glob)
  Andy Default <default@nowhere.net>: Second one / bbb.txt
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/ccc/one (glob)
  Andy Default <default@nowhere.net>: Second one / c-one.txt
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/ccc/two (glob)
  Andy Default <default@nowhere.net>: Second one / c-two.txt

Filenames are resolved against repo root.

  $ hg alld log first.txt 
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/aaa (glob)
  Andy Default <default@nowhere.net>: First file in aaa / first.txt
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/bbb (glob)
  Andy Default <default@nowhere.net>: First file in bbb / first.txt
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/ccc/one (glob)
  Andy Default <default@nowhere.net>: First file in ccc/one / first.txt
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/ccc/two (glob)
  Andy Default <default@nowhere.net>: First file in ccc/two / first.txt

  $ hg alldir heads -t
  => all_dirs: Executing heads in /tmp/cramtests-*/basic.t/work/aaa (glob)
  Andy Default <default@nowhere.net>: Second one / aaa.txt
  => all_dirs: Executing heads in /tmp/cramtests-*/basic.t/work/bbb (glob)
  Andy Default <default@nowhere.net>: Second one / bbb.txt
  => all_dirs: Executing heads in /tmp/cramtests-*/basic.t/work/ccc/one (glob)
  Andy Default <default@nowhere.net>: Second one / c-one.txt
  => all_dirs: Executing heads in /tmp/cramtests-*/basic.t/work/ccc/two (glob)
  Andy Default <default@nowhere.net>: Second one / c-two.txt

Global options

  $ hg -v --debug alldirs status 
  all_dirs: _parse called with args "?\[b?'-v', b?'--debug', b?'alldirs', b?'status'\]"? (re)
  all_dirs: initial parse succeeded, some trivial command
  all_dirs: finished parsing. Returning wrapper for status command
  => all_dirs: Executing status in /tmp/cramtests-*/basic.t/work/aaa (glob)
  all_dirs: return status: 0
  => all_dirs: Executing status in /tmp/cramtests-*/basic.t/work/bbb (glob)
  all_dirs: return status: 0
  => all_dirs: Executing status in /tmp/cramtests-*/basic.t/work/ccc/one (glob)
  all_dirs: return status: 0
  => all_dirs: Executing status in /tmp/cramtests-*/basic.t/work/ccc/two (glob)
  all_dirs: return status: 0

Errors

  $ hg alldirs log -r niematakiego
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/aaa (glob)
  abort: unknown revision 'niematakiego'!
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/bbb (glob)
  abort: unknown revision 'niematakiego'!
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/ccc/one (glob)
  abort: unknown revision 'niematakiego'!
  => all_dirs: Executing log in /tmp/cramtests-*/basic.t/work/ccc/two (glob)
  abort: unknown revision 'niematakiego'!
  abort: all_dirs: Executed command failed in:
  - /tmp/cramtests-*/basic.t/work/aaa (glob)
  - /tmp/cramtests-*/basic.t/work/bbb (glob)
  - /tmp/cramtests-*/basic.t/work/ccc/one (glob)
  - /tmp/cramtests-*/basic.t/work/ccc/two (glob)
  
  [255]

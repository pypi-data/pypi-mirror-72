
Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  $ . $TESTDIR/support/common.sh

First we need appropriate Mercurial configuration file (and variable
which ensures it is used).

  $ export HGRCPATH=$WORK_DIR/hgrc
  $ mkdir -p $HGRCPATH

  $ cat > $HGRCPATH/basic-local.rc << EOF
  > [ui]
  > username = Andy Default <default@nowhere.net>
  > logtemplate = {author}: {desc} / {files}\n
  > [extensions]
  > mercurial_on_remote =
  > EOF

Check help formatting:

  $ hg help onremote | head -1
  hg onremote REMOTE-NAME ANY-MERCURIAL-COMMAND [COMMAND-ARGS]

Create some repositories, and fill something there.
We are to use mostly ccc which will have aaa as default
and bbb as bbb.

  $ cd $WORK_DIR

  $ hg init aaa

  $ cd $WORK_DIR/aaa
  $ echo A > a.txt
  $ hg add a.txt
  $ hg commit -m 'AaA'

  $ echo B > b.txt
  $ hg add b.txt
  $ hg commit -m 'BbB'

  $ cd $WORK_DIR
  $ hg clone $WORK_DIR/aaa $WORK_DIR/bbb
  updating to branch default
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ cd $WORK_DIR
  $ hg clone $WORK_DIR/aaa ccc
  updating to branch default
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ cd $WORK_DIR/ccc

  $ cat >> .hg/hgrc <<END
  > [paths]
  > beee=$WORK_DIR/bbb
  > END

  $ hg paths
  beee = /*/work/bbb (glob)
  default = /*/work/aaa (glob)

and slight changes so repos vary:

  $ cd $WORK_DIR/aaa
  $ echo X > x.txt
  $ hg add x.txt
  $ hg commit -m 'XxX'

  $ cd $WORK_DIR/bbb
  $ echo Y > y.txt
  $ hg add y.txt
  $ hg commit -m 'YyY'

onremote in action (on files)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's start from some trivial commands

  $ cd $WORK_DIR/ccc

  $ hg onremote default root
  /*/work/aaa (glob)

  $ hg onremote beee root
  /*/work/bbb (glob)

and by direct path (not that it makes much sense)

  $ hg onremote $WORK_DIR/aaa root
  /*/work/aaa (glob)

  $ hg onremote $WORK_DIR/bbb root
  /*/work/bbb (glob)

Now something slightly more complicated, command with arguments

  $ hg onremote default log -l 2 -T 'Node:{node} Files:{files}\n'
  Node:* Files:x.txt (glob)
  Node:* Files:b.txt (glob)

  $ hg onremote beee log -l 2 -T 'Node:{node} Files:{files}\n'
  Node:* Files:y.txt (glob)
  Node:* Files:b.txt (glob)

and the same with more irritating template:

  $ hg onremote default log -l 2 -T 'Node: "{node}"\nFiles: "{files}"\n\n'
  Node: "[a-f0-9]{40}" (re)
  Files: "x.txt"
  
  Node: "[a-f0-9]{40}" (re)
  Files: "b.txt"
  

  $ hg onremote default log -l 2 -T "Node: '{node}'\nFiles: '{files}'\n\n"
  Node: '[a-f0-9]{40}' (re)
  Files: 'x.txt'
  
  Node: '[a-f0-9]{40}' (re)
  Files: 'b.txt'
  

Let's do sth active. Tag is simple, commit more difficult.

  $ echo ZZZ >> $WORK_DIR/aaa/a.txt
  $ echo TTT >> $WORK_DIR/bbb/b.txt

  $ hg onremote default status
  M a.txt
  $ hg onremote beee status
  M b.txt

  $ hg onremote default commit -m "Added some file, 'zzz' it's called\nHopefully it will help.\n"
  $ hg onremote beee commit -m "Added another one"

  $ hg onremote default tag vA.a
  $ hg onremote beee tag vB.b

and some verification

  $ hg onremote default tags
  tip                                4:* (glob)
  vA.a                               3:* (glob)

  $ hg onremote beee tags
  tip                                4:* (glob)
  vB.b                               3:* (glob)

  $ hg onremote default log -l3 -v
  Andy Default <default@nowhere.net>: Added tag vA.a for changeset * / .hgtags (glob)
  Andy Default <default@nowhere.net>: Added some file, 'zzz' it's called\nHopefully it will help.\n / a.txt
  Andy Default <default@nowhere.net>: XxX / x.txt

  $ hg onremote beee log -l3 -v
  Andy Default <default@nowhere.net>: Added tag vB.b for changeset * / .hgtags (glob)
  Andy Default <default@nowhere.net>: Added another one / b.txt
  Andy Default <default@nowhere.net>: YyY / y.txt

And let's throw some options consumed by onremote. They shouldn't matter.

  $ hg --verbose onremote default status 

  $ hg onremote default --verbose status  

  $ hg onremote beee --ssh some/ssh --quiet log -l 1 
  Andy Default <default@nowhere.net>: Added tag vB.b for changeset * / .hgtags (glob)

For the sake of it

  $ hg onremote beee incoming default
  comparing with /*/work/aaa (glob)
  searching for changes
  Andy Default <default@nowhere.net>: XxX / x.txt
  Andy Default <default@nowhere.net>: Added some file, 'zzz' it's called\nHopefully it will help.\n / a.txt
  Andy Default <default@nowhere.net>: Added tag vA.a for changeset * / .hgtags (glob)

  $ hg onremote default outgoing $WORK_DIR/ccc
  comparing with /*/work/ccc (glob)
  searching for changes
  Andy Default <default@nowhere.net>: XxX / x.txt
  Andy Default <default@nowhere.net>: Added some file, 'zzz' it's called\nHopefully it will help.\n / a.txt
  Andy Default <default@nowhere.net>: Added tag vA.a for changeset * / .hgtags (glob)

what if we start with cwd?

  $ cd $WORK_DIR

  $ hg --cwd $WORK_DIR/ccc  onremote beee log -l1
  Andy Default <default@nowhere.net>: Added tag vB.b for changeset * / .hgtags (glob)

Errors and their handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now some errors, to check how we react to them:

- running onremote outside repository

  $ hg onremote beee log -l 1
  abort: no repository found in '/*/work' (.hg not found)! (glob)
  [255]

  $ hg onremote ccc status
  abort: no repository found in '/*/work' (.hg not found)! (glob)
  [255]

- unknown options

  $ cd $WORK_DIR/ccc

  $ hg onremote --unknown default status >$OUT 2>$ERR
  [255]

  $ cat $ERR
  hg onremote: invalid arguments (option --unknown instead of remote name)

  $ cat $OUT
  hg onremote REMOTE-NAME ANY-MERCURIAL-COMMAND [COMMAND-ARGS]
  
  options:
  
   -e --ssh CMD       specify ssh command to use
      --remotecmd CMD specify hg command to run on the remote side
      --insecure      do not verify server certificate (ignoring web.cacerts
                      config)
  
  \(use ['"]hg onremote -h['"] to show more help\) (re)

  $ hg onremote -X --unknown default status  >$OUT 2>$ERR
  [255]

  $ cat $ERR
  hg onremote: invalid arguments (option -X instead of remote name)

  $ cat $OUT
  hg onremote REMOTE-NAME ANY-MERCURIAL-COMMAND [COMMAND-ARGS]
  
  options:
  
   -e --ssh CMD       specify ssh command to use
      --remotecmd CMD specify hg command to run on the remote side
      --insecure      do not verify server certificate (ignoring web.cacerts
                      config)
  
  \(use ['"]hg onremote -h['"] to show more help\) (re)

- unknown remote

  $ hg onremote koza status  >$OUT 2>$ERR
  [255]

  $ cat $ERR
  abort: repository koza (does not exist!|not found.*) (re)

  $ cat $OUT

  $ hg onremote koza log -l 4  >$OUT 2>$ERR
  [255]

  $ cat $ERR
  abort: repository koza (does not exist!|not found.*) (re)

  $ cat $OUT

- missing remote

  $ hg onremote   >$OUT 2>$ERR
  [255]

  $ cat $ERR
  hg onremote: invalid arguments (missing remote name)

  $ cat $OUT
  hg onremote REMOTE-NAME ANY-MERCURIAL-COMMAND [COMMAND-ARGS]
  
  options:
  
   -e --ssh CMD       specify ssh command to use
      --remotecmd CMD specify hg command to run on the remote side
      --insecure      do not verify server certificate (ignoring web.cacerts
                      config)
  
  \(use ['"]hg onremote -h['"] to show more help\) (re)

- missing command

  $ hg onremote default   >$OUT 2>$ERR
  [255]

  $ cat $ERR
  hg onremote: command to run not specified

  $ cat $OUT
  hg onremote REMOTE-NAME ANY-MERCURIAL-COMMAND [COMMAND-ARGS]
  
  options:
  
   -e --ssh CMD       specify ssh command to use
      --remotecmd CMD specify hg command to run on the remote side
      --insecure      do not verify server certificate (ignoring web.cacerts
                      config)
  
  \(use ['"]hg onremote -h['"] to show more help\) (re)

  $ hg onremote beee -l 3 >$OUT 2>$ERR
  [255]

  $ cat $OUT
  hg onremote REMOTE-NAME ANY-MERCURIAL-COMMAND [COMMAND-ARGS]
  
  options:
  
   -e --ssh CMD       specify ssh command to use
      --remotecmd CMD specify hg command to run on the remote side
      --insecure      do not verify server certificate (ignoring web.cacerts
                      config)
  
  \(use ['"]hg onremote -h['"] to show more help\) (re)

  $ cat $ERR
  hg onremote: invalid arguments (option -l not recognized)

- bad options of remote command

  $ hg onremote default log --ultradynamicate    >$OUT 2>$ERR
  [255]

  $ cat $ERR
  hg log: option --ultradynamicate not recognized

  $ cat $OUT | head -5
  hg log [OPTION]... [FILE]
  
  show revision history of entire repository or files
  
  options ([+] can be repeated):

- unsupported remote type

  $ hg onremote http://bitbucket.com/Mekk/on_remote status >$OUT 2>$ERR
  [255]

  $ cat $ERR
  abort: onremote: unsupported remote location type (expected ssh or local directory): http://bitbucket.com/Mekk/on_remote!

  $ cat $OUT



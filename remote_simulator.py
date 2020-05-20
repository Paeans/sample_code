
import os, sys
import subprocess
import shlex

import time

mlist = [''.join(['00', str(x+1)])[-2:] for x in range(21)]
plist = []

for mid in mlist:
  if mid in ['09', '33']:
    continue
  cmd_line = 'ssh -p 222 -o ConnectTimeout=5 -t            \
                 gpan@l-1d43-' + mid +                        \
                 ' \'bash -ic                                 \
                 "date; cd simulator.dnn;                     \
                 python test.py m' + mid + ' 10 10 10;                 \
                 date;" \''
  print(cmd_line)
  proc = subprocess.Popen(
    shlex.split('ssh -p 222 -o ConnectTimeout=5 -t            \
                 gpan@l-1d43-' + mid +                        \
                 ' \'bash -ic                                 \
                 "date; cd simulator.dnn;                     \
                 python test.py m' + mid + ' 10 10 10;                 \
                 date;" \''),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    close_fds = True)
  plist.append(proc)

index = 0
while(not all(x is None for x in plist)):
  if index >= len(plist):
    time.sleep(1)
    index %= len(plist)
  
  proc = plist[index]
  if proc == None or proc.poll() == None:
    index += 1
    continue
  
  output = proc.stdout.read()
  print(output)
  
  plist[index] = None
  index += 1


import os, shlex
import subprocess
import time

import numpy as np


def update_testFC (RA,TMR,testnum):
	ff=open("testFC.py", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'RA=' in line:
			data[i-1]='RA=' + str(RA) +'\n'
		if  'TMR=' in line:
			data[i-1]='TMR=' + str(TMR) +'\n'
		if  'testnum=' in line:
			data[i-1]='testnum=' + str(testnum) +'\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()


def update_diff1 (gain1):
	ff=open("diff1.sp", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'R3' in line:
			data[i-1]='R3 n1 out ' + str(gain1) +'k\n'
		if  'R4' in line:
			data[i-1]='R4 n2 0 ' + str(gain1) +'k\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()

def update_diff2 (gain2):
	ff=open("diff2.sp", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'R3' in line:
			data[i-1]='R3 n1 out ' + str(gain2) +'k\n'
		if  'R4' in line:
			data[i-1]='R4 n2 0 ' + str(gain2) +'k\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()

def update_diff3 (gain3):
	ff=open("diff3.sp", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'R3' in line:
			data[i-1]='R3 n1 out ' + str(gain2) +'k\n'
		if  'R4' in line:
			data[i-1]='R4 n2 0 ' + str(gain2) +'k\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()

def update_diff4 (gain4):
	ff=open("diff4.sp", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'R3' in line:
			data[i-1]='R3 n1 out ' + str(gain2) +'k\n'
		if  'R4' in line:
			data[i-1]='R4 n2 0 ' + str(gain2) +'k\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()

def update_diff5 (gain5):
	ff=open("diff5.sp", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'R3' in line:
			data[i-1]='R3 n1 out ' + str(gain2) +'k\n'
		if  'R4' in line:
			data[i-1]='R4 n2 0 ' + str(gain2) +'k\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()

testnum=10   #This is NOT a tunable parameter, it is just the number of test inputs you want to use from MNIST data set; Its max value is 10000
#The lower the testnum is the faster the optimization but it might not be accurate since you are not using the entire dataset



RA=10e-12   #ranges from 5e-12 to 20e-12 with "5e-12" steps 
TMR=100	    #ranges from 100 to 400 with "50" steps
gain1=10    #ranges from 5 to 20 with "1" steps
gain2=10    #ranges from 5 to 20 with "1" steps
gain3=10    #ranges from 5 to 20 with "1" steps
gain4=10    #ranges from 5 to 20 with "1" steps
gain5=10    #ranges from 5 to 20 with "1" steps

update_testFC (RA,TMR,testnum)

# sections to do
init_pers = 10
gene_num = 5
cut_pcent = 90

sproc_num = 8

drift_array = np.array(
        [[0, 0, 0, 0],
          [5, 5, 5, 0],
          [20, 20, 20, 0]])

n_size = 100000
rand_noise = np.random.normal(0, 10, n_size).astype(int)

sproc_num = 8
sproc_list = {x:None for x in range(sproc_num)} # id : proc.pid
pers_list = {x:None for x in range(sproc_num)}  # id : pers

def test_sproc(new_ppl):
  tag = False
  for key in sproc_list.keys():
    if sproc_list[key] == None:
      continue
    tag = True
    proc = sproc_list[key]
    if proc.poll() == None:
      continue
    output = proc.stdout.read().split('\n')
    pers = pers_list[key]
    pers[3] = float(output[0].split('=')[1]) * testnum
  return tag

def test_sproc_val(new_ppl):
  test_sproc(new_ppl)
  for key in sproc_list.keys():
    if sproc_list[key] == None:
      return True
  return False


def test_quality(pers):
  # set gain1 gain2 gain3
  update_diff1 (pers[0])
  update_diff2 (pers[1])
  update_diff2 (pers[2])
  
  # os.system('python testFC.py')
  print('<<<<<< output <<<<<<')
  print(pers)
  output = os.popen('python testFC.py | grep " = " '
                  ).read().split('\n')
  print(output)                
  err_rate = float(output[0].split('=')[1]) * testnum
  pers[3] = err_rate
  return err_rate


# section to do multiple process
def invoke_proc(pers):
  pid = -1
  for key in sproc_list.keys():
    if sproc_list[key] == None:
      pid = key
      break
  if pid == -1:
    return None
  curr_dir = os.getcwd()
  os.chdir('Simulator_DNN_' + str(pid))
  
  # set gain1 gain2 gain3
  update_diff1 (pers[0])
  update_diff2 (pers[1])
  update_diff2 (pers[2])
  
  # os.system('python testFC.py')
  print('<<<<<< output <<<<<<')
  print(pers)
  
  proc = subprocess.Popen(
      shelx.split('python testFC.py | grep " = " '), 
      stdout = subprocess.PIPE,
      close_fds = True)
  sproc_list[pid] = proc
  pers_list[pid] = pers
  os.chdir(curr_dir)
  return proc


# initial 10 population
print('****** initialize 16 population ******')

ppl = np.empty((16,0), int)
for i in range(4):
  ppl = np.concatenate((ppl, np.random.choice(range(16), 16, replace = False).reshape((16, 1))), axis = 1)
# ppl = np.random.randint(16, size = (init_pers, 4)) + 5

ppl = ppl + 5
ppl[:, 3] = 0
for pers in ppl:
  test_quality(pers)
  
print('<<<<<< the generation and min err rate is {} {} <<<<<<'.format(0, np.amin(ppl[:, 3])))

geni = 1
for gen in range(gene_num):
  print('****** new generation {} ******'.format(geni))
  # generate random pair
  ppl_num = ppl.shape[0]
  if ppl_num == 0:
    break
  '''
  rand_pair = np.random.choice(
        range(ppl_num), 
        ppl_num - ppl_num % 2, 
        replace = False).reshape(ppl_num // 2, 2)
  '''
  sorted_score = ppl[:, 3].argsort()[::-1]
  rand_pair = np.concatenate(
        (np.expand_dims(sorted_score[1:], axis = 1),
        np.expand_dims(sorted_score[:-1], axis = 1)),
        axis = 1)
        
  new_ppl = np.empty((0, 4), int)
  for pair in rand_pair:    
    pers1 = ppl[pair[0]]
    pers2 = ppl[pair[1]]
    '''
    d_pers = (pers1 + pers2) // 2
    for drift in drift_array:
      new_pers = (d_pers + drift) // 2
      if any((ppl[:, 0:3] == new_pers[0:3]).all(axis = 1)):
        print('>>>>>> generate one that already exists >>>>>>')
        continue
      test_quality(new_pers)
      new_ppl = np.concatenate((new_ppl, [ new_pers ]))
    '''
    new_pers = np.choose(np.random.randint(2, size = (4,)), 
                  np.concatenate(
                    ([pers1],
                    [pers2]), axis = 0))
    counter = 0
    while counter < n_size:
      r_pos = np.random.randint(n_size, size = (4,))
      tmp_pers = new_pers + [
            rand_noise[r_pos[0]], 
            rand_noise[r_pos[1]], 
            rand_noise[r_pos[2]], 
            rand_noise[r_pos[3]]]
      counter += 1
      if any(tmp_pers[0:3] > 20) or any(tmp_pers[0:3] < 5) or any((ppl[:, 0:3] == tmp_pers[0:3]).all(axis = 1)):
          print('>>>>>> generate one that already exists >>>>>>')
          continue
      new_pers = tmp_pers
      
      break
    new_ppl = np.concatenate((new_ppl, [ new_pers ]))
  
  new_ppl[:,3] = 0
  for new_pers in new_ppl:
  
    sproc_aval = test_sproc_val(new_ppl)  

    while not sproc_aval:      
      time.sleep(2.5 * testnum)
      sproc_aval = test_sproc_val(new_ppl)
      
    invoke_proc(new_pers)
  # new_ppl = np.concatenate((new_ppl, [ new_pers ]))  
  
  while test_sproc(new_ppl):
    time.sleep(2.5 * testnum)
  # generate produce
  
  ppl = np.concatenate((ppl, new_ppl))
  cutoff = np.percentile(ppl[:,3], cut_pcent, axis = 0)
  # purge population
  ppl = ppl[np.where(ppl[:, 3] <= cutoff)]
  print('<<<<<< the population after {} generation <<<<<<'.format(geni)) 
  print(ppl)
  print('<<<<<< the generation and min err rate is {} : {} / {} <<<<<<'.format(geni, np.amin(ppl[:, 3]), testnum))
  # print(ppl[np.where(ppl[:, 3] == np.amin(ppl[:, 3]))])
    
  geni += 1
  
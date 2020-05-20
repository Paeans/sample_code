
import argparse
import numpy as np

from argparse import RawTextHelpFormatter
from Bio import SeqIO

parser = argparse.ArgumentParser(formatter_class = RawTextHelpFormatter)
parser.add_argument("-f", "--fasta", help = "input fasta file", required=True)
parser.add_argument("-p", "--positions", help = "a file that contains list of positions", required=True)
parser.add_argument("-l", "--length", help = "length of the flanking sequence", type = int, required=True)
args = parser.parse_args()

seqs = list(SeqIO.parse(args.fasta, 'fasta'))

mutation = {'F3' : 0, 'U3' : 1, 'F5' : 2, 'U5' : 3, 'FSD' : 4, 'FSI' : 5,
            'IGR' : 6, 'IFD' : 7, 'IFI' : 8, 'ITR' : 9, 'MSM' : 10, 
            'NSM' : 11, 'NTM' : 12, 'RNA' : 13, 'SLT' : 14, 
            'SLR' : 15, 'SLS' : 16, 'TSS' : 17}

def get_chr(c):
  if c=='X':
    return 23
  elif c=='Y':
    return 24
  elif c=='M':
    return 25
  else:
    return int(c)

def one_hot_encode(seq):
  pass
    
pos_list = []

chrn = 0
index = 0
m_name = ''

with open(args.positions, 'r') as inFile:
  for line in inFile:
    position = line.strip().split();
    if get_chr(position[0]) == chrn and \
        int(position[1]) == index and \
        m_name == position[2]:
      continue
    pos_list.append([get_chr(position[0]), int(position[1]), position[2], position[3]]);
    chrn = get_chr(position[0])
    index = int(position[1])
    m_name = position[2]
pos_list.append([0, 0, '', ''])    
print(len(pos_list))

pos_array = np.zeros((len(pos_list) - 1, len(mutation)), dtype = float32)

start = 0
end = 0
flank = args.length // 2

for i in range(len(pos_list) - 1):
  chri = pos_list[i][0]
  posi = pos_list[i][1]
  
  while not (pos_list[start][0] == chri) or \
        posi - pos_list[start][1] > flank:
    start += 1
  if not (pos_list[end][0] == chri):
    end = i
  while pos_list[end][0] == chri and \
        pos_list[end][1] - posi < flank:
    end += 1
  t = start
  while t < end:
    pos_array[i][mutation[pos_list[t][2]]] += 1
    t += 1
    
  s = str(seqs[chri - 1].seq[posi - flank : posi + flank])

print(np.shape(pos_array))
np.savez('pos_array', pos = pos_array)




# UPDATE 12/20/2018: 
######## length leveled for b, l, and r.
from Bio import SeqIO
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument("-f", "--fasta", help = "input fasta file", required=True)
parser.add_argument("-p", "--positions", help = "a file that contains list of positions to extract flanking sequences", required=True)
parser.add_argument("-m", "--mode", help = "which flanking, r=right, l=left, b=both", type=str, choices=["r", "l", "b"], required=True)
parser.add_argument("-l", "--length", help = "length of the flanking sequence", type = int, required=True)
args = parser.parse_args()


seqs = list(SeqIO.parse(args.fasta, "fasta"))
positions = open (args.positions, "r")

def get_chr(c):
    if c=="X":
        return 23
    elif c=="Y":
        return 24
    elif c=="M":
        return 25
    else:
        return int(c)

output = open("human_"+args.mode+"_flanking_"+str(args.length)+".txt", 'w')
if args.mode == "r":
    #output = open("human_"+args.mode+"_flanking_"+str(args.length)+".txt", 'w')
    for line in positions:
        words=line.split()
        chr=get_chr(words[0])-1
        p=int(words[1])
        s=str(seqs[chr].seq[p:p+args.length])
        output.write (line.strip("\n").strip("\r")+"\t"+s+"\n")
    output.close()
    
if args.mode == "l":
    #output = open("human_"+args.mode+"_flanking_"+str(args.length)+".txt", 'w')
    for line in positions:
        words=line.split()
        chr=get_chr(words[0])-1
        p=int(words[1])
        s=str(seqs[chr].seq[p-args.length-1:p-1])
        output.write (line.strip("\n").strip("\r")+"\t"+s+"\n")
    output.close()


if args.mode == "b":
    #output = open("human_"+args.mode+"_flanking_"+str(args.length)+".txt", 'w')
    for line in positions:
        words=line.split()
        chr=get_chr(words[0])-1
        p=int(words[1])
        offset=args.length/2
        s=str(seqs[chr].seq[int(p-offset) : int(p+offset)]) # Yan used to write "[p-offset-1:p+offset]"
        output.write (line.strip("\n").strip("\r")+"\t"+s+"\n")
    output.close()
positions.close()
        

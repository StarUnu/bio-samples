# replica losresultados del paper:
# DNA sequence similarity analysis using image texture analysis based on first-order statistics

from sklearn.model_selection import KFold 
from sklearn.model_selection import train_test_split
#from matplotlib import pyplot as plt
#from matplotlib import cm
import matplotlib.pyplot as plt 
from matplotlib import pyplot
import math
import os
import sys
import cv2
import numpy as np
import math
from scipy.stats import kurtosis, skew
from Bio import SeqIO
import pandas as pd
import seaborn as sns

from descriptor import get_features
from descriptor import get_features_glcm
from descriptor import get_features_lbp
from descriptor import get_features_mlbp

from ete3 import PhyloTree, TreeStyle
from ete3 import Tree

from skbio import DistanceMatrix
from skbio.tree import nj


current_dir = os.path.dirname(os.path.abspath(__file__))

###################################################################################################################################
###################################################################################################################################

sequences = [   'J01859.fna',       'NR_037066.fna',        'NR_040849.fna',        'NR_117152.fna',    'NR_132306.fna', 
                'NR_134817.fna',    'NR_134818.fna',        'NR_136784.fna',        'NR_148244.fna',    'NR_148787.fna', 
                'NR_152063.fna',    'KP317497.fna',         'NR_156072.fna' ]

names    = [    'Escherichia coli', 'T.Thermophilus',       'B.Wakoensis',          'T.Filiformis',     'T.Tengchongensis', 
                'S.Cameli',         'S.Tangierensis',       'T.amyloliquefaciens',  'B.Xiamenensis',    'B.Australimaris', 
                'S.Halotolerans',   'B.Maritimus',          'S.Himalayensis']

csv_mega        = current_dir + "/sample_genomes/seqs_db1_distances.csv"
seq_file_full   = current_dir + "/sample_genomes/seqs_db1.fasta"
results_file    = current_dir + "/results/db1.png"
path_netwick    = 'newick_db1'

###################################################################################################################################
###################################################################################################################################

sequences = [   'L00016.fna',       'M22650.fna',           'M22651.fna',           'M22653.fna',       'M22654.fna', 
                'M22655.fna',       'M22656.fna',           'M22657.fna',           'V00658.fna',       'V00659.fna', 
                'V00672.fna',       'V00675.fna']

names    = [    'Human',            'Macaca mulatta',       'Macaca fuscata',       'Macaca fascicularis',  'Macaca sylvanus', 
                'Saimiri sciureus', 'Tarsius syrichta',     'Lemur catta',          'Gorilla',              'Hylobates', 
                'Chimpanzee',       'Sumatran Orangutan']

csv_mega        = current_dir + "/sample_genomes/seqs_db2_distances.csv"
seq_file_full   = current_dir + "/sample_genomes/seqs_db2.fasta"
results_file    = current_dir + "/results/db2.png"
path_netwick    = 'newick_db2'

###################################################################################################################################
###################################################################################################################################

sequences = [   'V00662.fna',       'D38116.fna',           'D38113.fna',           'D38114.fna',       'D38115.fna', 
                'X99256.fna',       'Y18001.fna',           'X79547.fna',           'Y07726.fna',       'X63726.fna', 
                'X72004.fna',       'U20753.fna',           'X61145.fna',           'X72204.fna',       'V00654.fna', 
                'X14848.fna',       'V00711.fna',           'X83427.fna']

names    = [    'Human',            'Pygmy chimpanzee',     'Common chimpanzee',    'Gorilla',              'Orangutan', 
                'Gibbon',           'Baboon',               'Horse',                'White rhinoceros',     'Harbor seal', 
                'Gray seal',        'Cat',                  'Fin whale',            'Blue whale',           'Cow', 
                'Rat',              'Mouse',                'Platypus']

csv_mega        = current_dir + "/sample_genomes/seqs_db3_distances.csv"
seq_file_full   = current_dir + "/sample_genomes/seqs_db3.fasta"
results_file    = current_dir + "/results/db3.png"
path_netwick    = 'newick_db3'


###################################################################################################################################
###################################################################################################################################

data_features = []
data_features_glcm = []
data_features_lbp = []
data_features_mlbp = []

f_out = open(seq_file_full, "w")

for sequence_file in sequences:

    f_in = open(current_dir + "/sample_genomes/" + sequence_file, "r")
    f_out.write(f_in.read())
    f_in.close()

    data = []    
    fa_file = current_dir + "/sample_genomes/" + sequence_file
    seqs = SeqIO.parse(fa_file, "fasta")
    for record in seqs:
        #print(record.id)
        #print(record.description)
        data.append(record.seq.upper())      

    seq = data[0]    

    skewness, my_kurtosis, energy, entropy = get_features(seq)
    data_features.append( [skewness, my_kurtosis, energy, entropy] )

    entropy, contrast, energy, correlation, homogeneity = get_features_glcm(seq)
    data_features_glcm.append( [entropy, contrast, energy, correlation, homogeneity] )

    hist_lbp = get_features_lbp(seq)
    data_features_lbp.append( hist_lbp )

    hist_mlbp = get_features_mlbp(seq)
    data_features_mlbp.append( hist_mlbp )
    #print([skewness, my_kurtosis, energy, entropy])
f_out.close()

data_features = np.array(data_features)
data_features_glcm = np.array(data_features_glcm)
data_features_lbp = np.array(data_features_lbp)
data_features_mlbp = np.array(data_features_mlbp)
#mean_seq = data_features[0]
#data_features = data_features[1:data_features.shape[0]]
#print(data_features)
#distances = []
#for features in data_features:
#    dist = np.sqrt(np.sum((mean_seq - features)**2))
#    distances.append(dist)
#distances = (distances - np.min(distances)) / (np.max(distances) - np.min(distances))

###################################################################################################################3
# procesamos las distancias entre todos los vectores
###################################################################################################################

# distance from first order statistics
DIST_proposed = np.zeros((data_features.shape[0], data_features.shape[0]))
for i in range(data_features.shape[0]):
    row = np.zeros(data_features.shape[0])
    for j in range(i, data_features.shape[0]):
        dist = np.sqrt(np.sum((data_features[i] - data_features[j])**2))
        row[j] = dist    
    DIST_proposed[i] = row

#copy the upper triangle to lower triangle in matrix
DIST_proposed = DIST_proposed + DIST_proposed.T - np.diag(np.diag(DIST_proposed))

DIST_proposed = (DIST_proposed - np.min(DIST_proposed)) / (np.max(DIST_proposed) - np.min(DIST_proposed))
distances_proposed = DIST_proposed[0,1:DIST_proposed.shape[0]]

####################################################################################
# distance from GLCM
DIST_proposed_glcm = np.zeros((data_features_glcm.shape[0], data_features_glcm.shape[0]))
for i in range(data_features_glcm.shape[0]):
    row = np.zeros(data_features_glcm.shape[0])
    for j in range(i, data_features_glcm.shape[0]):
        dist = np.sqrt(np.sum((data_features_glcm[i] - data_features_glcm[j])**2))
        row[j] = dist    
    DIST_proposed_glcm[i] = row

#copy the upper triangle to lower triangle in matrix
DIST_proposed_glcm = DIST_proposed_glcm + DIST_proposed_glcm.T - np.diag(np.diag(DIST_proposed_glcm))

DIST_proposed_glcm = (DIST_proposed_glcm - np.min(DIST_proposed_glcm)) / (np.max(DIST_proposed_glcm) - np.min(DIST_proposed_glcm))
distances_proposed_glcm  = DIST_proposed_glcm[0,1:DIST_proposed_glcm.shape[0]]
###################################################################################################################
###################################################################################################################

####################################################################################
# distance from LBP
DIST_proposed_lbp = np.zeros((data_features_lbp.shape[0], data_features_lbp.shape[0]))
for i in range(data_features_lbp.shape[0]):
    row = np.zeros(data_features_lbp.shape[0])
    for j in range(i, data_features_lbp.shape[0]):
        dist = np.sqrt(np.sum((data_features_lbp[i] - data_features_lbp[j])**2))
        row[j] = dist    
    DIST_proposed_lbp[i] = row

#copy the upper triangle to lower triangle in matrix
DIST_proposed_lbp = DIST_proposed_lbp + DIST_proposed_lbp.T - np.diag(np.diag(DIST_proposed_lbp))

DIST_proposed_lbp = (DIST_proposed_lbp - np.min(DIST_proposed_lbp)) / (np.max(DIST_proposed_lbp) - np.min(DIST_proposed_lbp))
distances_proposed_lbp  = DIST_proposed_lbp[0,1:DIST_proposed_lbp.shape[0]]
###################################################################################################################
###################################################################################################################

####################################################################################
# distance from MLBP
DIST_proposed_mlbp = np.zeros((data_features_mlbp.shape[0], data_features_mlbp.shape[0]))
for i in range(data_features_mlbp.shape[0]):
    row = np.zeros(data_features_mlbp.shape[0])
    for j in range(i, data_features_mlbp.shape[0]):
        dist = np.sqrt(np.sum((data_features_mlbp[i] - data_features_mlbp[j])**2))
        row[j] = dist    
    DIST_proposed_mlbp[i] = row

#copy the upper triangle to lower triangle in matrix
DIST_proposed_mlbp = DIST_proposed_mlbp + DIST_proposed_mlbp.T - np.diag(np.diag(DIST_proposed_mlbp))

DIST_proposed_mlbp = (DIST_proposed_mlbp - np.min(DIST_proposed_mlbp)) / (np.max(DIST_proposed_mlbp) - np.min(DIST_proposed_mlbp))
distances_proposed_mlbp  = DIST_proposed_mlbp[0,1:DIST_proposed_mlbp.shape[0]]
###################################################################################################################
###################################################################################################################


###################################################################################################################
###                    distances from mega              ###########################################################
###################################################################################################################
mega_dist_csv = pd.read_csv(csv_mega)  
mega_dist_csv = mega_dist_csv.set_index(mega_dist_csv.columns[0])
DIST_mega = mega_dist_csv.values
DIST_mega[np.isnan(DIST_mega)] = 0 # lllenamos con ceros los valores nan
DIST_mega = DIST_mega + DIST_mega.T #copiamos el triangulo inferior al superir en la matriz
distances_mega = DIST_mega[0,1:DIST_mega.shape[0]]

distances_mega = (distances_mega - np.min(distances_mega)) / (np.max(distances_mega) - np.min(distances_mega))
###################################################################################################################
###################################################################################################################


names_temp = np.array(sequences)
names_temp = names_temp[1:names_temp.shape[0]] # eliminamos el primer elemento
#print(names)

plt.clf()

#plt.plot(names_temp, distances_proposed, label='FOS', alpha=0.65)
#plt.plot(names_temp, distances_proposed_glcm, label='GLCM', alpha=0.65)
#plt.plot(names_temp, distances_proposed_lbp, label='LBP', alpha=0.65)
#plt.plot(names_temp, distances_mega, label='MEGA')
#plt.xticks(rotation=45, horizontalalignment='right', fontweight='light', fontsize=6 )
#plt.legend(loc='upper right')

fig, axs = plt.subplots(4)
axs[0].plot(names_temp, distances_proposed, 'b--', label='FOS')
axs[0].plot(names_temp, distances_mega, 'r-.', label='CLUSTALW')
axs[0].legend(loc='upper right', fontsize=6)
#axs[0].set_title('First order statistics')
axs[1].plot(names_temp, distances_proposed_glcm, 'b--', label='GLCM')
axs[1].plot(names_temp, distances_mega, 'r-.', label='CLUSTALW')
axs[1].legend(loc='upper right', fontsize=6)
#axs[1].set_title('First order statistics')
axs[2].plot(names_temp, distances_proposed_lbp, 'b--', label='LBP')
axs[2].plot(names_temp, distances_mega, 'r-.', label='CLUSTALW')
axs[2].legend(loc='upper right', fontsize=6)
#axs[1].set_title('First order statistics')
axs[3].plot(names_temp, distances_proposed_mlbp, 'b--', label='MLBP')
axs[3].plot(names_temp, distances_mega, 'r-.', label='CLUSTALW')
axs[3].legend(loc='upper right', fontsize=6)
#axs[1].set_title('First order statistics')


#for ax in axs.flat:
#    ax.set(xlabel='Sequence', ylabel='Distance', fontsize=6)
plt.xlabel('Sequences', fontsize=6)
#plt.ylabel('Distances', fontsize=6)

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()
    ax.yaxis.set_tick_params(labelsize=6)
#plt.tick_params(axis='both', which='minor', labelsize=6)

plt.xticks(rotation=45, horizontalalignment='right', fontweight='light', fontsize=6 )

#fig.text(0.5, 0.04, 'Sequence', ha='center')
fig.text(0.04, 0.5, 'Distances', va='center', rotation='vertical', fontsize=6 )

plt.savefig( results_file, dpi = 200, bbox_inches='tight')


###################################################################################################################
##########                   phylogenetics              ###########################################################
###################################################################################################################

dm = DistanceMatrix(DIST_proposed, sequences)
tree = nj(dm)
#print(tree.ascii_art())
newick_str_fos = nj(dm, result_constructor=str)
t = PhyloTree(newick_str_fos)
f = open(current_dir + "/results/" + path_netwick + "/fos.txt", "w")
f.write(newick_str_fos)
f.close()
#t.show()

dm = DistanceMatrix(DIST_proposed_glcm, sequences)
tree = nj(dm)
#print(tree.ascii_art())
newick_str_glcm = nj(dm, result_constructor=str)
t = PhyloTree(newick_str_glcm)
f = open(current_dir + "/results/" + path_netwick + "/glcm.txt", "w")
f.write(newick_str_glcm)
f.close()
#t.show()

dm = DistanceMatrix(DIST_proposed_lbp, sequences)
tree = nj(dm)
#print(tree.ascii_art())
newick_str_lbp = nj(dm, result_constructor=str)
t = PhyloTree(newick_str_lbp)
f = open(current_dir + "/results/" + path_netwick + "/lbp.txt", "w")
f.write(newick_str_lbp)
f.close()
#t.show()

dm = DistanceMatrix(DIST_proposed_mlbp, sequences)
tree = nj(dm)
#print(tree.ascii_art())
newick_str_mlbp = nj(dm, result_constructor=str)
t = PhyloTree(newick_str_mlbp)
f = open(current_dir + "/results/" + path_netwick + "/mlbp.txt", "w")
f.write(newick_str_mlbp)
f.close()
#t.show()

dm = DistanceMatrix(DIST_mega, sequences)
tree = nj(dm)
print(tree.ascii_art())
newick_str_mega = nj(dm, result_constructor=str)
t = PhyloTree(newick_str_mega)
f = open(current_dir + "/results/" + path_netwick + "/mega.txt", "w")
f.write(newick_str_lbp)
f.close()
#t.show()



t1 = Tree(newick_str_mega)
t2 = Tree(newick_str_fos)
t3 = Tree(newick_str_glcm)
t4 = Tree(newick_str_lbp)
t5 = Tree(newick_str_mlbp)
#print(t1.robinson_foulds(t2, unrooted_trees=True))
rf_fos, rf_max_fos, *_  = t1.robinson_foulds(t2, unrooted_trees=True)
rf_glcm, rf_max_glcm, *_  = t1.robinson_foulds(t3, unrooted_trees=True)
rf_lbp, rf_max_lbp, *_  = t1.robinson_foulds(t4, unrooted_trees=True)
rf_mlbp, rf_max_mlbp, *_  = t1.robinson_foulds(t5, unrooted_trees=True)
print ("RF distance is %s over a total of %s" %(rf_fos, rf_max_fos))
print ("RF distance is %s over a total of %s" %(rf_glcm, rf_max_glcm))
print ("RF distance is %s over a total of %s" %(rf_lbp, rf_max_lbp))
print ("RF distance is %s over a total of %s" %(rf_mlbp, rf_max_mlbp))

# distances first dataset
#RF distance is 14 over a total of 20
#RF distance is 18 over a total of 20
#RF distance is 18 over a total of 20
#RF distance is 12 over a total of 20

# distances second dataset
#RF distance is 12 over a total of 18
#RF distance is 18 over a total of 18
#RF distance is 18 over a total of 18
#RF distance is 16 over a total of 18

# distances third dataset
#RF distance is 14 over a total of 30
#RF distance is 30 over a total of 30
#RF distance is 30 over a total of 30
#RF distance is 26 over a total of 30

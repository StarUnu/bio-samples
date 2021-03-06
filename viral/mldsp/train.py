# MLDSP: machine learning with DIgiral Signal Processing
# A python implementation of MLDSP

import numpy as np
from Bio import SeqIO
from Bio import Phylo

import re
import sys
import glob
import statistics
import pywt
#from sympy import fft es muy lento
from scipy.fftpack import fft
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.model_selection import train_test_split
import joblib
import os

from skbio import DistanceMatrix
from skbio.tree import nj
from ete3 import PhyloTree, TreeStyle

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import matplotlib.cm as cm

from random import randint



 
def cmdscale(D):
    """                                                                                       
    Classical multidimensional scaling (MDS)                                                  
                                                                                               
    Parameters                                                                                
    ----------                                                                                
    D : (n, n) array                                                                          
        Symmetric distance matrix.                                                            
                                                                                               
    Returns                                                                                   
    -------                                                                                   
    Y : (n, p) array                                                                          
        Configuration matrix. Each column represents a dimension. Only the                    
        p dimensions corresponding to positive eigenvalues of B are returned.                 
        Note that each dimension is only determined up to an overall sign,                    
        corresponding to a reflection.                                                        
                                                                                               
    e : (n,) array                                                                            
        Eigenvalues of B.                                                                     
                                                                                               
    """
    # Number of points                                                                        
    n = len(D) 
    # Centering matrix                                                                        
    H = np.eye(n) - np.ones((n, n))/n 
    # YY^T                                                                                    
    B = -H.dot(D**2).dot(H)/2 
    # Diagonalize                                                                             
    evals, evecs = np.linalg.eigh(B) 
    # Sort by eigenvalue in descending order                                                  
    idx   = np.argsort(evals)[::-1]
    evals = evals[idx]
    evecs = evecs[:,idx] 
    # Compute the coordinates using positive-eigenvalued components only                      
    w, = np.where(evals > 0)
    L  = np.diag(np.sqrt(evals[w]))
    V  = evecs[:,w]
    Y  = V.dot(L)
 
    return np.matrix(Y), evals


def numMappingPP(nucleotide):
    if nucleotide == 'A':
        return -1
    elif nucleotide == 'C':
        return 1
    elif nucleotide == 'G':
        return -1
    elif nucleotide == 'T':
        return 1

# original matlan function
# function [AcNmb, Seq, numberOfClusters, clusterNames, pointsPerCluster] = readFasta(dataSet)
# AcNmb: list of seqId de todas
# Seq: list of sequences in the dataset de todas
# numberOfClusters: numero de clases
# clusterNames: clases
# muestras por clase
def readFasta(path_database, database):
    path = path_database + '/' + database

    number_of_clases = 0
    cluster_names = []
    points_per_cluster = []
    sequences = []
    str_all = ""
    
    #print(glob.glob(path + '/*' ))
    clusters = glob.glob(path + '/*' )
    number_of_clases = len(clusters)
    for cluster in clusters:
        cluster_name = cluster.split('/')[-1]
        cluster_names.append( cluster_name )

        # read each fasta file
        files = clusters = glob.glob(cluster + '/*.txt' )
        points_per_cluster.append(len(files))
        
        # read sequences from each file, the majority have one sequence per file          
        for file in files:        
            seqs = SeqIO.parse(file, "fasta") 
                      
            for record in seqs:
                sequences.append([record.id, record.seq.upper(), cluster_name])      
                str_all += ">" +   record.id + "\n"   +  str(record.seq.upper()) + "\n"       

    sequences_mat = np.array(sequences)

    return sequences_mat, number_of_clases, cluster_names, points_per_cluster, str_all



# Compute the magnitud spectrum of FFT of a numerical sequence
# seq: sequence, string of letters A, C, G, T
# median_len: median size of all sequences in a dataset
def descriptor(seq, median_len):
    ns  = list(map(numMappingPP, seq))  # here we map the nucleotides to numbers

    ## we ensure that all the sequences have the same size 
    I   = median_len - len(ns) # change "median_len" to other length stat for length normalization
    if I > 0: # when the seq size is smaller than the median
        ns_temp = pywt.pad(ns, I, 'antisymmetric') #wextend('1','asym',ns,I);
        ns_temp = np.array(ns_temp)
        #print(len(ns_temp), len(ns))
        ns_new = ns_temp[I:ns_temp.shape[0]] #nsNew = nsTemp((I+1):length(nsTemp));        
    elif I < 0: # when the seq size is bigger than the median
        ns = np.array(ns)
        ns_new = ns[0:median_len]
    else:
        ns_new = np.array(ns)

    #print(ns_new.shape)
    #print("processing FFT...")
    fourier_transform = fft(ns_new)
    #print("getting  magnitude spectra...")
    magnitud_spectra = np.abs(fourier_transform) # %magnitude spectra

    return  ns_new, fourier_transform, magnitud_spectra


if __name__ == "__main__" :
    path_database = '/home/vicente/projects/BIOINFORMATICS/MLDSP/DataBase'
    database_name = 'Influenza'
    path_database = sys.argv[1]
    database_name = sys.argv[2]



    # read fasta ej folder jerarqui proposed by LSDSP
    sequences, number_of_clases, cluster_names, points_per_cluster, str_all = readFasta(path_database, database_name)

    #calculate length stats
    sequences_size  = list(map(len, sequences[:, 1]))
    total_seq       = len(sequences_size)

    max_len     = max(sequences_size)
    min_len     = min(sequences_size)
    mean_len    = int(statistics.mean(sequences_size))
    median_len  = int(statistics.median(sequences_size))
    #print("max_len, min_len, mean_len, median_len ", max_len, min_len, mean_len, median_len)

    nm_val_SH     = []
    f           = []
    lg          = []

    print('Generating numerical sequences, applying DFT, computing magnitude spectra ...')

    for seq in sequences[:, 1]:
        ns_new, fourier_transform, magnitud_spectra = descriptor(seq, median_len)
        
        nm_val_SH.append(ns_new)
        f.append(fft(fourier_transform))
        lg.append(magnitud_spectra)
        

    #################################################################################################
    # distance calculation by Pearson correlation coefficient
    print('Computing Distance matrix .... ...')

    # pandas version
    #lg_df = pd.DataFrame(np.transpose(lg)) # transpose in order to compute PCC by observation
    #pearsoncorr = lg_df.corr(method='pearson')  #Pearson correlation coefficient [-1 1]
    #dist_mat = (1 - pearsoncorr)/2  #  normalize between 0 and 1

    # numpy version
    pearsoncorr = np.corrcoef(np.matrix(lg))
    dist_mat = (1 - pearsoncorr)/2

    # testing Pearson Correlation Distance
    #X = [[1460, 517.201, 230.163, 453.649, 266.169, 267.257], [1340, 569.351, 219.907, 473.615, 239.587, 229.557], [1462, 622.617, 324.276, 503.927, 214.432,223.652], [1994, 672.012, 456.685, 412.211, 219.068, 131.52]]
    #X_pd = pd.DataFrame(np.transpose(np.matrix(X)))
    #X_corr = X_pd.corr(method='pearson')
    #X_corr_norm = (1 - X_corr)/2

    #X_corr_2 = np.corrcoef(np.matrix(X))
    #X_corr_norm_2 = (1 - X_corr_2)/2
    ##################################################################################################
    # train

    kf = KFold(n_splits=5)
    X = dist_mat
    y = sequences[:, 2]

    clf = svm.SVC(kernel='linear', C=1)
    scores = cross_val_score(clf, X, y, cv=5)
    print("scores cv=5", scores)
    print("mean score", statistics.mean(scores))

    # thain the whole database
    clf = svm.SVC(kernel='linear', C=1)
    clf.fit(X, y)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = current_dir + '/models/' + database_name
    joblib.dump(clf, file_name + ".sav")
    np.savetxt(file_name + "_magnitud_spectrum.csv", lg, delimiter=',', fmt='%f')

    print(len(lg), " features")

    '''
    for train_index, test_index in kf.split(dist_mat):
        print('TRAIN:', train_index, 'TEST:', test_index)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
    '''
    
    sys.exit()

    #########################################################################################################
    # phylogenetic tree
    # check simetry
    # some elements in diagonal are close to zero
    # dist_mat = np.around(dist_mat, decimals=5)

    for i in range(dist_mat.shape[0]):
        #if dist_mat[i][i] != 0.0:
        #    print(i, " ", dist_mat[i][i])

        dist_mat[i][i] = 0.0


    asym = dist_mat - dist_mat.T
    asym_ = np.where(asym != 0.0, 1, 0)
    print(" no simetric distances:", np.sum(asym_))

    dist_mat = dist_mat+ dist_mat.T - np.diag(np.diag(dist_mat))

    asym = dist_mat - dist_mat.T
    asym_ = np.where(asym != 0.0, 1, 0)
    print(" no simetric distances:", np.sum(asym_))

    #print(dist_mat)
    dm = DistanceMatrix(dist_mat, sequences[:, 0])
    tree = nj(dm)
    #print(tree.ascii_art())
    newick_str = nj(dm, result_constructor=str)
    #print(newick_str)
    #print(newick_str[:55], "...")
    #print(str_all)
    t = PhyloTree(newick_str)
    #t.link_to_alignment(alignment=str_all, alg_format="fasta")
    t.show()


    #########################################################################################################
    # Classical multidimentional scaling
    Y, evals = cmdscale(dist_mat)
    print("dist_mat.shape:", dist_mat.shape)
    print("Y.shape:", Y.shape)

    ax = plt.axes(projection='3d')

    # Data for a three-dimensional line
    #zline = np.linspace(0, 15, 1000)
    #xline = np.sin(zline)
    #yline = np.cos(zline)
    #ax.plot3D(xline, yline, zline, 'gray')

    # Data for three-dimensional scattered points
    zdata = Y[:,0]
    xdata = Y[:,1]
    ydata = Y[:,2]

    #import itertools
    #colors = itertools.cycle(["r", "b", "g"])
    colors = cm.rainbow(np.linspace(0, 1, number_of_clases))
    
    
    print(points_per_cluster)
    print(xdata.shape)
    tmp = 0
    for i in range(number_of_clases):        
        ini = tmp
        end = ini + points_per_cluster[i]
        #print(ini, end)
        #ax.scatter3D(xdata[ini:end], ydata[ini:end], zdata[ini:end], alpha=0.6, c=next(colors))
        ax.scatter3D(xdata[ini:end], ydata[ini:end], zdata[ini:end], alpha=0.6, c=colors[i], label=cluster_names[i])
        tmp = end 
        
    ax.legend()   
  
    plt.show()

    #number_of_clases, cluster_names, points_per_cluster
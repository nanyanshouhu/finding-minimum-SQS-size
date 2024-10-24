# finding-minimum-SQS-size
The Special Quasirandom Structure (SQS) is a concept used in computational materials science to model disordered solid solutions, alloys, and mixed systems. It aims to represent the average properties of a random solid solution using a small, ordered supercell that mimics the correlation functions of a fully random system. Finding the smallest and most optimal SQS supercell can significantly reduce computational costs. However, for some non-equiatomic compositions, it is difficult to determine the appropriate size of the SQS supercell while still satisfying the frequency of pair, triplet, and quadruplet correlations. 
This program will help you find the minimum size of the supercell size for the SQS generation by using the Alloy Theoretic Automated Toolkit (ATAT). 

Input file "rndstr.in" 
Here is an example of rndstr.in: 

example 1 (fcc non-equiatomic fcc quaternary alloy)

3.54 3.54 3.54  90 90 90
0 0.5 0.5
0.5 0 0.5
0.5 0.5 0
0.000000000000   0.000000000000   0.000000000000 Fe=0.4, Ni=0.3, Co=0.2, Cr=0.1  

example 2 (non-equiatomic high entropy pervosite)
3.94 3.94 3.94 90 90 90
1 0 0
0 1 0
0 0 1
0.5 0.5 0.5 Co=0.8,Fe=0.2
0 0 0 La=0.2,Sr=0.2,Ba=0.2,Y=0.2,Pr=0.2
0.5 0 0 O=1
0 0.5 0 O=1
0 0 0.5 O=1

# how to execute the code

1. Make sure the “rndstr.in” file is the same directory
2. run the command "python minimum_size_sqs.py"

# output information for example 2
Original Mixed Count: 2                                              # the number of mixed type
Mix Fractions: [[0.8, 0.2], [0.2, 0.2, 0.2, 0.2, 0.2]]             # the mix fraction
Combination Size: 2                                               # the maxium combination you considered: pair=2, triplet=3, quadruplet=4
Minimum Denominators (per site): [25, 25] 
Target Mixed Atoms (per site): [25, 25]                                   # the minimum number of atoms for each mixed site
LCM of Target Mixed Atoms: 25
Species Count: {'Co=0.8,Fe=0.2': 25, 'La=0.2,Sr=0.2,Ba=0.2,Y=0.2,Pr=0.2': 25, 'O=1': 75}
Total Atoms: 125                                                         # The total number of atoms in SQS
Scaling Factor (LCM): 25

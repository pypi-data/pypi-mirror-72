import pandas as pd
import numpy as np
import string as stringmod
    
def random_bipartite(N_A,N_B,N_L,name_A=None,name_B=None,multigraph=False):    
    
    ##################
    # Initial Checks #
    ##################
    
    if N_A<=0 or N_B<=0:
        raise ValueError('Number of nodes and edges must be positive.')
    
    if N_L<=0:
        raise ValueError('Inputs resulted in no edges.')
        
    if not np.max([N_A,N_B])<=N_L:
        raise ValueError('Number of nodes on each side must be at least the number of edges.')
        
    if name_A is None:
        name_A = 'A'
    if name_B is None:
        name_B = 'B'
    
    if not isinstance(name_A, str)  or not isinstance(name_A, str):
        raise ValueError('name_A, name_B must be string')
    if name_A==name_B:
        raise ValueError('name_A must be different from name_B')
    
        
    ################################
    # Pre-processing the variables #
    ################################    
        
    N_A = int(N_A)
    N_B = int(N_B)
    N_L = int(N_L)
    
    group_name_A = name_A.upper()
    group_name_B = name_B.upper()
    node_name_A  = name_A.lower() 
    node_name_B  = name_B.lower() 
    
    prefix_min_side = node_name_A if N_A<N_B else node_name_B
    prefix_max_side = node_name_B if N_A<N_B else node_name_A
    
    N_min = np.min([N_A,N_B])
    N_max = np.max([N_A,N_B])
    
    ################################
    # Filling the edges            #
    ################################   
    
    # Filling edges in 3 steps:
    # E1: connecting all nodes from N_min side
    # E2: connecting N_max-N_min nodes from N_max side
    # E3: connecting the remaining N_L - N_max
    
    # E1: Fill the first N_min edges 
    table_E1 = pd.DataFrame(columns=['min','max'])
    table_E1['min'] = [prefix_min_side+'%d'%(i+1) for i in range(N_min)]
    table_E1['max'] = [prefix_max_side+'%d'%(i+1) for i in range(N_min)]
    
    # E2
    table_E2 = pd.DataFrame(columns=['min','max'])
    table_E2['min'] = np.random.choice(table_E1['min'],size=(N_max-N_min))
    table_E2['max'] = [prefix_max_side+'%d'%(i+N_min+1) for i in range(N_max-N_min)]
    
    # E3
    table_E3 = pd.DataFrame(columns=['min','max'])
    if N_L > N_max:
        table_E3['min'] = np.random.choice(table_E1['min'],size=(N_L-N_max))
        table_E3['max'] = np.random.choice(pd.concat([table_E1['max'],table_E2['max']],axis=0),size=(N_L-N_max))
        
    # Concatenating the tables from the 3 stages
    table = pd.concat([table_E1,table_E2,table_E3],axis=0,ignore_index=True)
    
    # This is perfectible !!!!!!!!
    # We are randomizing the whole of E3 when only one edge repeated
    # Ideally: uniform random sampling of random bipartite space
    # Sub-optimal but better: choose at random, but edge by edge
    while table.duplicated().any() and (not multigraph): 
        table_E3['max'] = np.random.choice(pd.concat([table_E1['max'],table_E2['max']],axis=0),size=(N_L-N_max))
        table = pd.concat([table_E1,table_E2,table_E3],axis=0,ignore_index=True)
    
    ################################
    # Formatting the output table  #
    ################################   
    
    # Renaming columns
    if N_A<N_B:
        rename_dic = {'min':group_name_A,'max':group_name_B}
    else:
        rename_dic = {'max':group_name_A,'min':group_name_B}
    table.rename(columns=rename_dic,inplace=True)
    table = table[[group_name_A,group_name_B]]
    
    # Putting in HINPY format
    table['start_group'] = group_name_A
    table['end_group'] = group_name_B
    table['relation'] = group_name_A+'-'+group_name_B
    table['value'] = ''
    table['timestamp'] = ''
    table.rename(columns={group_name_A:'start_object',group_name_B:'end_object'},inplace=True)
    table = table[['relation','start_group','start_object','end_group','end_object','value','timestamp']]

    return table;

def random_concatenated_bipartites(list_N_nodes,list_N_edges,list_names=None,multigraph=False): 

    ##################
    # Initial Checks #
    ##################
    
    if list_names is None:
        alphabet_list = list(stringmod.ascii_lowercase)
        if len(list_N_nodes)>len(alphabet_list):
            raise ValueError('list_N_nodes has more elements than letters in the alphabet. Naming not yet implemented! Sorry.')
        list_names = alphabet_list[:len(list_N_nodes)]
        
    if not len(list_N_nodes)==len(list_N_edges)+1    :
        raise ValueError('list_N_nodes must have exactly 1 more element than list_N_edges.')
    
    if len(list(set(list_names)))!=len(list_names):    
        raise ValueError('list_names contains at least one repeated element.')
        
    if len(list_N_nodes) != len(list_names):
        raise ValueError('list_N_nodes must have the same length as list_names')
         

    ########################
    # Creating  bipartites #
    ########################
        
    ## Creating empty table    
    table = pd.DataFrame(columns=['relation','start_group','start_object','end_group','end_object','value','timestamp'])
        
        
    for i in range(0,len(list_N_edges)):
        
        ##  Create bi-partite table for N_L(i) 
        table_aux = random_bipartite(list_N_nodes[i],list_N_nodes[i+1],list_N_edges[i],
                                     name_A=list_names[i],name_B=list_names[i+1],multigraph=multigraph)

        ## Concatenate to table
        table = pd.concat([table,table_aux],axis=0,ignore_index=True)
    
    return table;


    





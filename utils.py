
'''
 TKG-ACLED-GTA-Dataset
	  
  File:     utils.py
  Authors:  Julia Gastinger (julia.gastinger@neclab.eu)

NEC Laboratories Europe GmbH, Copyright (c) 2023, All rights reserved.  

       THIS HEADER MAY NOT BE EXTRACTED OR MODIFIED IN ANY WAY.
 
       PROPRIETARY INFORMATION ---  

SOFTWARE LICENSE AGREEMENT

ACADEMIC OR NON-PROFIT ORGANIZATION NONCOMMERCIAL RESEARCH USE ONLY

BY USING OR DOWNLOADING THE SOFTWARE, YOU ARE AGREEING TO THE TERMS OF THIS
LICENSE AGREEMENT.  IF YOU DO NOT AGREE WITH THESE TERMS, YOU MAY NOT USE OR
DOWNLOAD THE SOFTWARE.

This is a license agreement ("Agreement") between your academic institution
or non-profit organization or self (called "Licensee" or "You" in this
Agreement) and NEC Laboratories Europe GmbH (called "Licensor" in this
Agreement).  All rights not specifically granted to you in this Agreement
are reserved for Licensor. 

RESERVATION OF OWNERSHIP AND GRANT OF LICENSE: Licensor retains exclusive
ownership of any copy of the Software (as defined below) licensed under this
Agreement and hereby grants to Licensee a personal, non-exclusive,
non-transferable license to use the Software for noncommercial research
purposes, without the right to sublicense, pursuant to the terms and
conditions of this Agreement. NO EXPRESS OR IMPLIED LICENSES TO ANY OF
LICENSOR'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. As used in this
Agreement, the term "Software" means (i) the actual copy of all or any
portion of code for program routines made accessible to Licensee by Licensor
pursuant to this Agreement, inclusive of backups, updates, and/or merged
copies permitted hereunder or subsequently supplied by Licensor,  including
all or any file structures, programming instructions, user interfaces and
screen formats and sequences as well as any and all documentation and
instructions related to it, and (ii) all or any derivatives and/or
modifications created or made by You to any of the items specified in (i).

CONFIDENTIALITY/PUBLICATIONS: Licensee acknowledges that the Software is
proprietary to Licensor, and as such, Licensee agrees to receive all such
materials and to use the Software only in accordance with the terms of this
Agreement.  Licensee agrees to use reasonable effort to protect the Software
from unauthorized use, reproduction, distribution, or publication. All
publication materials mentioning features or use of this software must
explicitly include an acknowledgement the software was developed by NEC
Laboratories Europe GmbH.

COPYRIGHT: The Software is owned by Licensor.  

PERMITTED USES:  The Software may be used for your own noncommercial
internal research purposes. You understand and agree that Licensor is not
obligated to implement any suggestions and/or feedback you might provide
regarding the Software, but to the extent Licensor does so, you are not
entitled to any compensation related thereto.

DERIVATIVES: You may create derivatives of or make modifications to the
Software, however, You agree that all and any such derivatives and
modifications will be owned by Licensor and become a part of the Software
licensed to You under this Agreement.  You may only use such derivatives and
modifications for your own noncommercial internal research purposes, and you
may not otherwise use, distribute or copy such derivatives and modifications
in violation of this Agreement.

BACKUPS:  If Licensee is an organization, it may make that number of copies
of the Software necessary for internal noncommercial use at a single site
within its organization provided that all information appearing in or on the
original labels, including the copyright and trademark notices are copied
onto the labels of the copies.

USES NOT PERMITTED:  You may not distribute, copy or use the Software except
as explicitly permitted herein. Licensee has not been granted any trademark
license as part of this Agreement.  Neither the name of NEC Laboratories
Europe GmbH nor the names of its contributors may be used to endorse or
promote products derived from this Software without specific prior written
permission.

You may not sell, rent, lease, sublicense, lend, time-share or transfer, in
whole or in part, or provide third parties access to prior or present
versions (or any parts thereof) of the Software.

ASSIGNMENT: You may not assign this Agreement or your rights hereunder
without the prior written consent of Licensor. Any attempted assignment
without such consent shall be null and void.

TERM: The term of the license granted by this Agreement is from Licensee's
acceptance of this Agreement by downloading the Software or by using the
Software until terminated as provided below.  

The Agreement automatically terminates without notice if you fail to comply
with any provision of this Agreement.  Licensee may terminate this Agreement
by ceasing using the Software.  Upon any termination of this Agreement,
Licensee will delete any and all copies of the Software. You agree that all
provisions which operate to protect the proprietary rights of Licensor shall
remain in force should breach occur and that the obligation of
confidentiality described in this Agreement is binding in perpetuity and, as
such, survives the term of the Agreement.

FEE: Provided Licensee abides completely by the terms and conditions of this
Agreement, there is no fee due to Licensor for Licensee's use of the
Software in accordance with this Agreement.

DISCLAIMER OF WARRANTIES:  THE SOFTWARE IS PROVIDED "AS-IS" WITHOUT WARRANTY
OF ANY KIND INCLUDING ANY WARRANTIES OF PERFORMANCE OR MERCHANTABILITY OR
FITNESS FOR A PARTICULAR USE OR PURPOSE OR OF NON- INFRINGEMENT.  LICENSEE
BEARS ALL RISK RELATING TO QUALITY AND PERFORMANCE OF THE SOFTWARE AND
RELATED MATERIALS.

SUPPORT AND MAINTENANCE: No Software support or training by the Licensor is
provided as part of this Agreement.  

EXCLUSIVE REMEDY AND LIMITATION OF LIABILITY: To the maximum extent
permitted under applicable law, Licensor shall not be liable for direct,
indirect, special, incidental, or consequential damages or lost profits
related to Licensee's use of and/or inability to use the Software, even if
Licensor is advised of the possibility of such damage.

EXPORT REGULATION: Licensee agrees to comply with any and all applicable
export control laws, regulations, and/or other laws related to embargoes and
sanction programs administered by law.

SEVERABILITY: If any provision(s) of this Agreement shall be held to be
invalid, illegal, or unenforceable by a court or other tribunal of competent
jurisdiction, the validity, legality and enforceability of the remaining
provisions shall not in any way be affected or impaired thereby.

NO IMPLIED WAIVERS: No failure or delay by Licensor in enforcing any right
or remedy under this Agreement shall be construed as a waiver of any future
or other exercise of such right or remedy by Licensor.

GOVERNING LAW: This Agreement shall be construed and enforced in accordance
with the laws of Germany without reference to conflict of laws principles.
You consent to the personal jurisdiction of the courts of this country and
waive their rights to venue outside of Germany.

ENTIRE AGREEMENT AND AMENDMENTS: This Agreement constitutes the sole and
entire agreement between Licensee and Licensor as to the matter set forth
herein and supersedes any previous agreements, understandings, and
arrangements between the parties relating hereto.

       THIS HEADER MAY NOT BE EXTRACTED OR MODIFIED IN ANY WAY.
'''


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from rdflib import Graph
import rdflib
import json


def df_to_rdfgraph(graph_df):
    g = Graph()
    triples = graph_df.to_numpy()

    for triple in triples:
        if 'http' in triple[0]: s = rdflib.term.URIRef(triple[0]) 
        else: s = rdflib.term.BNode(triple[0])
        if 'http' in triple[2]: o = rdflib.term.URIRef(triple[2]) 
        else: o = rdflib.term.BNode(triple[2])       
        g.add((s,rdflib.term.URIRef(triple[1]),o))
    return g

def map_ids_to_time(timesteps_range_all, timesteps_range):
    # create dicts that map the timesteps to numeric id, and other way round. 
    i = 0
    time_to_id = {}
    id_to_time = {}
    for t in timesteps_range_all:
        t = str(t.date())
        time_to_id[t] = i #lookup dict
        id_to_time[i] = t
        i+=1

    i = 0
    time_to_id_ourinterval = {}
    id_to_time_ourinterval = {}
    for t in timesteps_range:
        t = str(t.date())
        time_to_id_ourinterval[t] = i #lookup dict
        id_to_time_ourinterval[i] = t
        i+=1
    return time_to_id, id_to_time, time_to_id_ourinterval, id_to_time_ourinterval

def map_ids_to_string(added_dict, timesteps_range, task_name):
    # create dicts that map the node strings to numeric id, and other way round. same for relations
    # dump those dicts as json files
    # create stat.txt with number of nodes and number of relations

    all_nodes_set = set()
    all_relations_set = set()
    for t_all in timesteps_range: 
        t = str(t_all.date())
        if t in added_dict.keys():
            nodes =  [[i[0] , i[2]] for i in added_dict[t]]
            nodes_1d = [item for sublist in nodes for item in sublist]

            relations = [i[1] for i in added_dict[t]]

            all_nodes_set.update(nodes_1d)
            all_relations_set.update(relations)
    nodes =  [] #[[i[0] , i[2]] for i in static_list]
    nodes_1d = [item for sublist in nodes for item in sublist]

    relations = [] #[i[1] for i in static_list]

    all_nodes_set.update(nodes_1d)
    all_relations_set.update(relations)

    i = 0
    node_to_id = {}
    id_to_node = {}
    for node in all_nodes_set:
        node_to_id[node] = i #lookup dict
        id_to_node[i] = node
        i+=1

    rel_to_id = {}
    id_to_rel = {}
    i = 0
    for rel in all_relations_set:
        rel_to_id[rel] = i #lookup dict
        id_to_rel[i] = rel
        i+=1

    with open('./data/' + task_name+'node_to_id.json', 'a') as file:
        json.dump(node_to_id, file)
    with open('./data/' + task_name+'id_to_node.json', 'a') as file:
        json.dump(id_to_node, file)
    with open('./data/' + task_name+'rel_to_id.json', 'a') as file:
        json.dump(rel_to_id, file)
    with open('./data/' + task_name+'id_to_rel.json', 'a') as file:
        json.dump(id_to_rel, file)

    num_nodes = len(all_nodes_set)
    num_rels = len(all_relations_set)
    with open('./data/' + task_name+ '_stat.txt', 'a') as id_file:
            frame = {'num_nodes': pd.Series(num_nodes), 'num_rels': pd.Series(num_rels)}
            dframe =pd.DataFrame(frame)
            frame_str = dframe.to_string(header=False, index=False)
            id_file.write(frame_str)

    return node_to_id, rel_to_id

def create_dicts_from_df(datasetid_gta, datasetid_acled=None):
    # create a dict with key: timestamp, values: triples at that timestamp for both, acled and gta plus dataset identifier
    # read the specified csv files, use the columns of interest
    dataset_df_gta = pd.read_csv(datasetid_gta, keep_default_na=False)  # because it contains labels "NA" for Namibia, 
                                                                        # which will otherwise be interpreeted as nan
    dataset_df_acled = pd.read_csv(datasetid_acled, keep_default_na=False)

    # gta
    added_dict = {start_d: df[["0","1","2","6"]].values for start_d,df in dataset_df_gta.groupby("3")}
    # 6: gta string
    if '1000-03-03' in added_dict.keys():
        del added_dict['1000-03-03'] #remove the entries which have no announcement date

    # acled
    acled_ts_dict = {impl_d: df[["0","1","2","6"]].values for impl_d,df in dataset_df_acled.groupby("3")}
    # 6: acled string

    # combine both
    merged_dict = {}
    for key, val1 in added_dict.items():
        if key in acled_ts_dict.keys():
            merged_dict[key] = list(val1) + list(acled_ts_dict[key])
        else:
            merged_dict[key] = list(val1)
    for key2, val2 in acled_ts_dict.items(): # add the acled triples for not existing gta timestamps
        if key2 not in added_dict.keys():
            merged_dict[key2] = list(val2)    
    
    return merged_dict



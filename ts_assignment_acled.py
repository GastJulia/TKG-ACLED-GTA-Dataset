""""
TKG-ACLED-GTA-Dataset
	  
  File:     ts_assignment_acled.py
  Authors:  Julia Gastinger (julia.gastinger@neclab.eu)

NEC Laboratories Europe GmbH, Copyright (c) 2022, All rights reserved.  

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
"""
"""
## Create a csv file with all acled events and their dates

* read acled nt file (merged or not merged)
* extract all acled events and their dates
* create and store a csv file with all triples, their date, and dataset id

"""
# imports
from rdflib import Graph
import rdflib
import pandas as pd
from datetime import datetime
from copy import copy

def find_actors(s):
    # find all actors for a given node (list: actors_for_s)
    # find for each of these actors all the triples that belong to it (dict: actors_triples w key: actor, value: 
    # all triples with the actor as subject)
    actors_for_s = []
    actors_triples = {}

    for _, _, actor in g.triples((s, rdflib.term.URIRef('https://schema.coypu.org/global#hasActor'), None)): 
        # which triples have the given node as subjects, and the relation "hasActor"
        actors_for_s.append(str(actor)) # append the found actor
        actors_triples_list = []

        for s_actor, p_a, o_a in g.triples((actor, None, None)): # for the found actor: append all triples of interest to list
            if not 'label' in str(p_a): # we do not need the labels
                actors_triples_list.append([str(s_actor), str(p_a), str(o_a)])
            actors_triples[str(s_actor)] = actors_triples_list # add the list to a dictionary

    return actors_for_s, actors_triples

# load graph
g = Graph()
name = 'acled_subset'
if name =='acled_subset': # without merged acled events (ie all events)
    g.parse("./data/acled/acled_subset_2021.nt")
elif name =='acled_merged_subset': # with merged acled events
    g.parse("./data/acled/acled_merged_subset_2021.nt")

print("the length of the graph is: ", len(g))

#find all relations of any type
#find all nodes of any type
list_p = []
list_nodes = []

for s, p, o in g.triples((None,  None, None)):    
    list_p.append(p)
    list_nodes.append(s)
    list_nodes.append(o)

relation_set = set(list_p)
nodes_set = set(list_nodes)

print("Number of different relations before filter: ", len(relation_set))
print("Number of different nodes before filter: ", len(nodes_set))

# find all acled actors
actors = []
for node in nodes_set:
    if 'https://data.coypu.org/acled' in str(node):
        actors.append(node)
print("Number of acled actors:", len(actors))

# create dictionaries with 
# a) des_dict: all events and their event ids and timesteps
# b) actors_dict: key timesteps, values actors
# c) actors_triples_dict: all infos that we have for the actors
covered_events = [] #list of acled events we covered. for info only
des_dict ={} #dict with all events and their event ids and timesteps; key: event id
actors_dict={} #dict with keys: timesteps, values: actors
actors_triples_dict= {} # dict with keys: actors, values: all triples we have with the actor as suject
for s, p, o in g.triples((None,rdflib.term.URIRef('https://schema.coypu.org/global#hasTimestamp'), None)):
    # find each event that is subject to the triple hasTimestamp
    date_o = datetime.strptime(str(o), '%Y-%m-%d').date() # extract the timestamp

    event_id = str(s)
    if event_id not in des_dict.keys():     # add the event and the respective timestamps to a dictionary
        des_dict[event_id] = {}
    des_dict[event_id]['event'] = str(s)    
    des_dict[event_id]['Date'] = date_o     # add timestamp date

    covered_events.append(str(s)) 

    actors_for_event, actors_triples = find_actors(s)   # find all actors that belong to this event, and all triples 
                                                        # that have these actors as subjects
    for actor in actors_for_event:
        if str(date_o) in actors_dict.keys():
            actors_dict[str(date_o)].append(str(actor))
        else:
            actors_dict[str(date_o)] = [str(actor)]
        
        if actor not in actors_triples_dict.keys():
            actors_triples_dict[actor] = actors_triples[str(actor)]

covered_events_set = set(covered_events)
print("Number of covered events: ", len(covered_events_set))


# create graph (list) with all events and all the triples that have this event as subject
# the graph has subject, object, relation, date of the respective acled event, and identifiers: '0', '1', '1'. the identifier '1' is the acled identifier (as compared to '0' for gta)
# we exclude all triples that have the relation: hasTimestamp, hasLocation, comment, label because they are not needed
graph = []
for acled in list(des_dict.keys()): #[0:10]:
    for s, p, o in g.triples((rdflib.term.URIRef(acled), None, None)):
        if str(p) not in ['https://schema.coypu.org/global#hasTimestamp', 'https://schema.coypu.org/global#hasLocation', 'Thttp://www.w3.org/1999/02/22-rdf-syntax-ns#comment', 'http://www.w3.org/2000/01/rdf-schema#comment', 'http://www.w3.org/2000/01/rdf-schema#label' ]: # we do NOT need triples with the date
            graph.append([s, p, o, des_dict[acled]['Date'], '0', '0', '1']) #last entry: '1'is acled identifier'; zeros: placeholders to have same shape as gta
           
print('Number of triples in graph before appending actors info: ', len(graph))

# append actors information to the graph
for time, actors in actors_dict.items():
    for actor in actors:
        for trip in actors_triples_dict[actor]:
            quad = copy(trip)
            graph.append([quad[0], quad[1], quad[2], time, '0', '0', '1']) #last entry: '1'is acled identifier'; zeros: placeholders
            
print('Number of triples in graph after appending actors info: ', len(graph))

list_p = []
list_nodes = []
for s, p, o in graph[:,0:2]:    
    list_p.append(p)
    list_nodes.append(s)
    list_nodes.append(o)

relation_set = set(list_p)
nodes_set = set(list_nodes)

# save to csv
df_all = pd.DataFrame(graph)
df = df_all.drop_duplicates(keep='first') 
print("length of the graph after dropping duplicates is: ", df.shape)
if name =='acled_subset':
    df.to_csv('./data/acled/graph_acled_subset.csv', index=False)
elif name =='acled_merged_subset':
    df.to_csv('./data/acled/graph_acled_subset_merged.csv', index=False)




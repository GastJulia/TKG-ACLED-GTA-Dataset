"""
TKG-ACLED-GTA-Dataset
	  
  File:     ts_assignment_gta.py
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
Create a csv file with all gta interventions and state acts and their dates

* read gta nt file
* extract all state acts and interventions, and their announcement date
* create and store a csv file with all triples, their announcement date, implementation date, removal date, static/dynamic identifier, and dataset id
* create a csv file with static of all events for each timestep ()
"""

from rdflib import Graph
import rdflib
from datetime import datetime
import pandas as pd

# load graph
g = Graph()

name = 'gta_aggregated'

if name =='gta_aggregated':
    g.parse("./data/gta/gta_aggregated_2021.nt") 

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

print("Number of different relations: ", len(relation_set))
print("Number of different nodes: ", len(nodes_set))

# create dictionaries with 
# a) the interventions and their announcementdate, implememntationdate and removaldate (des_dict)
# b) the stateacts and their announcementdate, implementationdate and removaldate (of the latest removed intervention) (announcement_date_per_stateact, implementation_date_per_stateact, removal_date_per_stateact)
# if a intervention or announcement has no removal date: set default date 3000-03-03
# if a intervention or announcement has no start date: set default date 1000-03-03

# interventions
des_dict ={} # key: intervention str(subject); values: intervention and [event_id]['AnnouncementDate'] announcement date, implementation date, removal date

# state acts:
announcement_date_per_stateact ={} # key: stateact str(subject); value: announcement date
removal_date_per_stateact = {} # key: stateact str(subject); value:implementation date
implementation_date_per_stateact = {} # key: stateact str(subject); value: removal date
covered_stateactids = [] #list of all covered state acts

never_removed_date = datetime.strptime('3000-03-03', '%Y-%m-%d').date() # default date for events without removal date
never_added_date = datetime.strptime('1000-03-03', '%Y-%m-%d').date() # default date for events without start (announcement/implementation) date

# stati
status_events_dict = {}
status_state_ids_dict = {}
status_triple = ['has_status', 'announced', 0, 0, 0, 0,0, 'announced_start', 'announced_end', 'implemented_start', 'implemented_end']
 
# find each event that is subject to the triple hasImplementationDate (each Intervention):
for s, p, o in g.triples((None,rdflib.term.URIRef('https://schema.coypu.org/gta#hasImplementationDate'), None)):     
    date_o = datetime.strptime(str(o), '%Y-%m-%d').date() # extract the timestamp
    event_id = str(s) 
    if event_id not in des_dict.keys():     # add the event and the respective timestamps to a dictionary        
        des_dict[event_id] = {}
    des_dict[event_id]['event'] = str(s)

    # find the stateact that has the respective intervention as object
    stateactids = [s2 for s2,_,_ in g.triples((None, rdflib.term.URIRef('https://schema.coypu.org/gta#hasIntervention'), s))]

    # a) add announcement date:    
    if len(stateactids)>0:
        for stateactid in stateactids:           
            covered_stateactids.append(stateactid) # add the stateact to covered_stateactids
            AnnouncementDateList = [o2 for _,_,o2 in g.triples((stateactid, rdflib.term.URIRef('https://schema.coypu.org/gta#hasAnnouncementDate'), None))] # find the announcement date of that stateact
            announce_date = datetime.strptime(str(AnnouncementDateList[0]), '%Y-%m-%d').date()
            if len(AnnouncementDateList) > 0: 
                # a.1 for interventions:
                des_dict[event_id]['AnnouncementDate'] = announce_date  # add the announcement date to the des_dict
                # a.2 for state acts:
                announcement_date_per_stateact[stateactid] = announce_date                  # and to the state act dict

    else:
        print('no stateactid for event', str(s))

    # b) add implemenation date
    # b.1 for interventions:
    des_dict[event_id]['ImplementationDate'] = date_o    
    # b.2 for stateacts:
    # the implementation date of each state act is the implementation date of its first intervention-event 
    if stateactid in implementation_date_per_stateact.keys():
        if des_dict[event_id]['ImplementationDate'] < implementation_date_per_stateact[stateactid]:
            implementation_date_per_stateact[stateactid] = des_dict[event_id]['ImplementationDate']        
    else:
        implementation_date_per_stateact[stateactid] = des_dict[event_id]['ImplementationDate']

    # c) add removal date 
    # c.1 for interventions:
    RemovalDateList = [o3 for _,_,o3 in g.triples((s, rdflib.term.URIRef('https://schema.coypu.org/gta#hasRemovalDate'), None))]
    if len(RemovalDateList) > 0: des_dict[event_id]['RemovalDate'] = datetime.strptime(str(RemovalDateList[0]), '%Y-%m-%d').date()
    else: des_dict[event_id]['RemovalDate'] = never_removed_date # if it was never removed: add artificial removal date

    # c.2 removal dates for stateactids:
    # the removal date of each state act is the removal date of its latest intervention-event        
    if stateactid in removal_date_per_stateact.keys():
        if des_dict[event_id]['RemovalDate'] > removal_date_per_stateact[stateactid]:
            removal_date_per_stateact[stateactid] = des_dict[event_id]['RemovalDate'] 
    else:
        removal_date_per_stateact[stateactid] = des_dict[event_id]['RemovalDate']

    # d) stati for interventions: stat and end date of the announcement period and of the implementation period
    # if needed: uncomment
    # if announce_date < date_o:
    #     announced_start = announce_date
    #     announced_end = date_o
    # else:
    #     announced_start =never_added_date
    #     announced_end = never_added_date
    # implemented_start = date_o
    # implemented_end = des_dict[event_id]['RemovalDate']
    # status_triple = ['has_status', 'announced', 0, 0, 0, 0, 0, announced_start, announced_end, implemented_start, implemented_end]    
    # status_events_dict[event_id] = status_triple


covered_stateactids = set(covered_stateactids)

# e) add all state acts that have not been covered because their interventions have not been implemented yet:
for s, p, o in g.triples((None,rdflib.term.URIRef('https://schema.coypu.org/gta#hasAnnouncementDate'), None)):
    if s not in covered_stateactids:
        implementation_date_per_stateact[s] = never_removed_date # announced, never implemented
        announcement_date_per_stateact[s] = datetime.strptime(str(o), '%Y-%m-%d').date() 

# create graph with interventions
# we exclude all triples with time information, ie ImplementationDate and Removal Date (because we add time information manually)
# we exclude all triples with relations: label, InterventionId, StateActId, type, because we do not need these triples for analysis
graph = []
for gta in list(des_dict.keys()): #[0:10]:
    for s, p, o in g.triples((rdflib.term.URIRef(gta), None, None)):
        if str(p) not in ['https://schema.coypu.org/gta#hasRemovalDate', 'https://schema.coypu.org/gta#hasImplementationDate',
                          'http://www.w3.org/2000/01/rdf-schema#label', 'https://schema.coypu.org/gta#hasInterventionId', 
                          'https://schema.coypu.org/gta#hasStateActId', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type']: #  # we do NOT need triples with the date
            graph.append([s, p, o, des_dict[gta]['AnnouncementDate'], des_dict[gta]['ImplementationDate'], des_dict[gta]['RemovalDate'], '0']) # last entry: '0' for gta

# append stateact triples
# we exclude all triples with time information, ie AnnouncementDate, ImplementationDate and Removal Date (because we add time information manually)
# we exclude all triples with relations: label, InterventionId, StateActId, type, because we do not need these triples for analysis
for state_act in covered_stateactids:
    for s, p, o in g.triples((rdflib.term.URIRef(state_act), None, None)):
        if str(p) not in ['https://schema.coypu.org/gta#hasRemovalDate', 'https://schema.coypu.org/gta#hasImplementationDate', 
                          'https://schema.coypu.org/gta#hasAnnouncementDate', 
                          'http://www.w3.org/2000/01/rdf-schema#label', 'https://schema.coypu.org/gta#hasInterventionId', 
                          'https://schema.coypu.org/gta#hasStateActId', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type']: # we do NOT need triples with the date
            start_date = announcement_date_per_stateact[state_act]
            implementation_date = implementation_date_per_stateact[state_act]
            graph.append([s, p, o, start_date, implementation_date, removal_date_per_stateact[state_act], '0'])# last entry: '0' for gta

            # append static triples
for s, p, o in g.triples((None, None, None)):
    if 'https://data.coypu.org/country/' in str(s):
        graph.append([s, p, o, never_added_date, never_added_date, never_removed_date, '0'])#  last entry: '0' for gta
print("length of the graph is: ", len(graph))

## save to csv
df_all = pd.DataFrame(graph)
df = df_all.drop_duplicates(keep='first') 
print("length of the graph after dropping duplicates is: ", df.shape)
df.to_csv('./data/gta/graph_' + name + '.csv', index=False)

# for information only: find and print all types of state acts
types = []

for s, p, o in g.triples((None, rdflib.term.URIRef('https://schema.coypu.org/gta#hasInterventionType'), None)):
    types.append(str(o))#last entry: static:'1', not static:'0'

types_set = set(types)
print(types_set)

# event stati
# create a list with all stati and intervals for each intervention and state act
# if needed: uncomment

# f) stati for state acts: stat and end date of the announcement period and of the implementation period
# if needed: uncomment
# for stateact in covered_stateactids:
#     #events:
#     if announcement_date_per_stateact[stateact] < implementation_date_per_stateact[stateact]:
#         announced_start = announcement_date_per_stateact[stateact]
#         announced_end = implementation_date_per_stateact[stateact]
#     else:
#         announced_start =never_added_date
#         announced_end = never_added_date
#     implemented_start = implementation_date_per_stateact[stateact]
#     implemented_end = removal_date_per_stateact[stateact]
#     status_triple = ['has_status', 'announced', 0, 0, 0, 0, 0, announced_start, announced_end, implemented_start, implemented_end]    
#     status_state_ids_dict[stateact] = status_triple


# stati = []
# for stateid, values in status_state_ids_dict.items():
#     lis= [stateid]
#     lis.append(el for el in values)
#     stati.append([lis])

# eventstati = []
# for eventids, values in status_events_dict.items():
#     lis= [eventids]
#     lis.append(el for el in values)
#     eventstati.append([lis])

# if needed: uncomment: also save the stati of the events
# eventstati_df = pd.DataFrame(eventstati)
# eventstati_df.to_csv('./data/gta/graph_' + name + '_eventstati.csv', index=False)
# stati_df = pd.DataFrame(stati)
# stati_df.to_csv('./data/gta/graph_' + name + '_stateact_stati.csv', index=False)
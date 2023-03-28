'''
 TKG-ACLED-GTA-Dataset
	  
  File:     visualisation_demo.py
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


"""
Viewer class
"""
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import visdcc
import numpy as np
import json


def triples_to_cytoscape(triples):
    nodes = []
    edges = []
    for triple in triples:
        subj, pred, obj = str(triple[0]) or "??empty_subject", str(triple[1]) or "??empty_predicate", str(triple[2]) or "??empty_object"
        nodes += [subj, obj]
        edges.append({"source": subj, "target": obj, "label": pred})
    nodes = set(nodes)
    elements = [{"data": {"id": n, "label": n}} for n in nodes]
    elements += [{"data": e} for e in edges]
    return elements



def triples_to_visdcc_nodes_edges(triples, nodes_with_positions_dict=None):
    show_labels = False# show label strings instead of ids
    if show_labels:
        with open('./data/acled_subset_gta_aggregatedid_to_node.json') as f:
            nodes_to_labels = json.load(f)
    nodes = []
    nodes_acled = []
    nodes_gta = []
    edges = []
    for triple in triples:
        subj, pred, obj = str(triple[0]), str(triple[1]), str(triple[2])
        if str(triple[3]) == '1':
            nodes_acled += [subj, obj]
        else:
            nodes_gta += [subj, obj]
        edges.append({"from": subj, "to": obj, "label": pred})

    if show_labels:
        nodes_acled2 = [{"id": n, "label": nodes_to_labels[str(n)], "color": '#1F77B4'} for n in set(nodes_acled)] #acled nodes have color": '#1F77B4' (blue)
        nodes_gta2 = [{"id": n, "label": nodes_to_labels[str(n)], "color": '#FF7F0E'} for n in set(nodes_gta)] # gta nodes have color": '#FF7F0E'orange
    else:
        nodes_acled2 = [{"id": n, "label": n, "color": '#1F77B4'} for n in set(nodes_acled)] # acled nodes have color": '#1F77B4' (blue)
        nodes_gta2 = [{"id": n, "label": n, "color": '#FF7F0E'} for n in set(nodes_gta)]     # gta nodes have color": '#FF7F0E'orange


    nodes_both = []
    if len(triples) < 10000:
        for n in set(nodes_gta):
            if n in set(nodes_acled):
                if show_labels:
                    nodes_both.append({"id": n, "label": nodes_to_labels[str(n)], "color": '#2CA02C'}) # nodes that appear for both have color #2CA02C' -green
                else:
                    nodes_both.append({"id": n, "label": n, "color": '#2CA02C', 'borderWidth': '2'}) # nodes that appear for both have color #2CA02C' -green
    nodes = nodes_acled2 + nodes_gta2 +nodes_both
    if nodes_with_positions_dict != None:
        nodes = [{"id": node_key, "label": node_key, "x": nodes_with_positions_dict[node_key]['x'], "y": nodes_with_positions_dict[node_key]['y']} for node_key in set(nodes)]
    return {'nodes': nodes, 'edges': edges}


def read_triples(ts: int):
    data = np.loadtxt("./data/acled_subset_gta_aggregated_ids_graph.txt", dtype=int) 
    indic = [0,1,2,4]
    triples = [tuple(list(t[indic])) for t in data if ts<0 or  t[3] ==ts]
    if ts < 0:  # this takes a looooot of time
        triples = list(set(triples))  # remove duplicates if loading the whole file
    return triples


def layout():
    vis_options = {'height': '2000px', 'width': '80%','scale':50,
        'nodes': {  # https://visjs.github.io/vis-network/docs/network/nodes.html
            'widthConstraint': {'maximum': 600},
            'font': {'size': 5}
        },
        'edges': {
            'length': 300,
            'arrows': {
                'to': {'enabled': True}
            },
        },
    }

    rows = [
        html.H1("Demo"),
        visdcc.Network(id='my-graph', options=vis_options),
        dcc.Slider(-1, 364, 1, value=0, id='my-slider'),
        html.Button('save-x-y', id='debugbutton', n_clicks=0),
    ]

    return dbc.Container([dbc.Row(row, style={"marginTop": "10px"}) for row in rows])

@callback(
    Output('my-graph', 'run'),
    State('my-graph', 'data'), 
    Input("debugbutton", 'n_clicks'),
)
def debug(data, nclicks):
    if data is None:
        return ""
    javascript = "let positions = this.net.getPositions(); let pos = 0;\n"
    for node in data["nodes"]:
        node_id = node["id"]
        if node_id:
            javascript += f"pos = positions[{node_id}]; console.log({node_id} + ' - ' + pos.x + ' - ' + pos.y);\n"
    return javascript

@callback(
    Output('my-graph', 'data'),
    Input('my-slider', 'value'),
)
def change_timestamp(timestamp):
    triples = read_triples(timestamp)
    load = False
    if load == True:
        with open('nodes_positions.json') as json_file:
            nodes_with_positions = json.load(json_file)
    else:
        nodes_with_positions = None
    return triples_to_visdcc_nodes_edges(triples, nodes_with_positions)





if __name__ == "__main__":
    app = Dash(__name__, title="Graph Visualisation Demo", external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = layout()
    app.run_server(debug=True, host="0.0.0.0")

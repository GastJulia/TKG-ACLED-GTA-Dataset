'''
 TKG-ACLED-GTA-Dataset
	  
  File:     ts_analysis.py
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

import numpy as np
import seasonal
from networkx.algorithms import approximation as app
import networkx as nx
from matplotlib import pyplot as plt

class TsAnalyser():
    """ For time series extraction """
    def __init__(self, device='cpu'):
        self.device = device
        self.seasonal_markers_dict = {}

    def preprocess_dataset(self, timesteps_all, graph_dict, dataset_name):
        graph_ts = list(graph_dict.keys())

        self._timestep_indexer = {value: idx for idx, value in enumerate(timesteps_all)}  # maps ts2indeces
        self._timestep_indexer_inv = {idx: value for idx, value in enumerate(timesteps_all)}  # maps indeces2ts

        all_features = self.extract_timeseries_from_graphs(graph_dict) 
        # extract: [num_triples_all, num_nodes, max_deg, mean_deg, mean_deg_c, max_deg_c, min_deg_c, density]

        self._min_list_from_train = [np.min(all_features[i]) for i in range(len(all_features))]
        self._max_list_from_train = [np.max(all_features[i]) for i in range(len(all_features))]

        seasonality =self.estimate_seasons(all_features[0])     # estimate seasonality 

        # create seasonal markers dict (for all timesteps)
        seasonal_markers_dict = self.assign_seasonal_markers(timesteps_all, seasonality)         
        self.seasonal_markers_dict = seasonal_markers_dict

        names = ['Number of Triples', 'Number of Nodes', 'Max Node Degree', 'Mean Node Degree',         
                 'Mean Degree Centrality', 'Max Degree Centrality', 'Min Degree Centrality', 'Density']

        for timeseries, name in zip(all_features, names):
            self.plot_feature_figure(timesteps_all, timeseries, name, seasonality, dataset_name)

        feature_extension_dict = self.extend_features(seasonal_markers_dict, all_features, graph_ts)        

        return seasonality, seasonal_markers_dict, feature_extension_dict

        

    def extend_features(self, seasonal_markers_dict, all_features, timesteps_of_interest):
        """ dict with key: timestep, values: all the extended features.
        """

        extended_features = {}
        for ts in timesteps_of_interest:
            index = self._timestep_indexer[ts]
            features_ts = [all_features[feat][index] for feat in range(len(all_features))]
            features_ts.append(seasonal_markers_dict[ts])
            extended_features[ts] = features_ts
        
        return extended_features

    def extract_timeseries_from_graphs(self, graph_dict):
        """ extracts multivariate timeseries from quadruples based on graph params

        :param graph_dict: dict, with keys: timestep, values: triples; training quadruples.

        """
        num_nodes = []
        num_triples = []
        max_deg = []
        mean_deg = []
        mean_deg_c = [] 
        max_deg_c = [] 
        min_deg_c = [] 
        density = []

        for ts, triples_snap in graph_dict.items():

            # create graph for that timestep
            e_list_ts = [(triples_snap[line][0], triples_snap[line][2]) for line in range(len(triples_snap))]
            G = nx.MultiGraph()
            G.add_nodes_from(graph_dict[ts][:][ 0])
            G.add_nodes_from(graph_dict[ts][:][2])
            G.add_edges_from(e_list_ts)  # default edge data=1

            # extract relevant parameters and append to list
            num_nodes.append(G.number_of_nodes())
            num_triples.append(G.number_of_edges())

            # degree
            deg_list = list(dict(G.degree(G.nodes)).values())
            max_deg.append(np.max(deg_list))
            mean_deg.append(np.mean(deg_list))
            
            # degree centrality
            deg_clist = list(dict(nx.degree_centrality(G)).values())
            mean_deg_c.append(np.mean(deg_clist))
            max_deg_c.append(np.max(deg_clist))
            min_deg_c.append(np.min(deg_clist))
            
            density.append(nx.density(G))
 
        return [num_triples, num_nodes, max_deg, mean_deg, mean_deg_c, max_deg_c, min_deg_c, density]

    def estimate_seasons(self, train_data):
        """ Estimate seasonal effects in a series.
               
        Estimate the major period of the data by testing seasonal differences for various period lengths and returning 
        the seasonal offsets that best predict out-of-sample variation.   
            
        First, a range of likely periods is estimated via periodogram averaging. Next, a time-domain period 
        estimator chooses the best integer period based on cross-validated residual errors. It also tests
        the strength of the seasonal effect using the R^2 of the leave-one-out cross-validation.

        :param data: list, data to be analysed, time-series;
        :return: NBseason int. if no season found: 1; else: seasonality that was discovered (e.g. if seven and 
                time granularity is daily: weekly seasonality)
        """
        seasons, trended = seasonal.fit_seasons(train_data)
        
        if seasons is None:
            Nbseason = int(1)
        else: 
            Nbseason = len(seasons)
            
        return Nbseason

    def extract_num_triples(self, triple_dict):
        num_triples_all = []
        for graph in triple_dict.values():
            num_triples_all.append(len(graph))
        return num_triples_all

    def assign_seasonal_markers(self, timesteps_all, seasonality):
        """ lookup dict that says which element of a seasonal period we are in for each timestep.
        e.g. timestep[0]:0 ( monday);  timestep[1]:1 ( tuesday); ...  timestep[7]:0 ( monday)
        :param timesteps_all: list with timesteps
        :param seasonality: int, seasonality that we have (e.g. if seven and time granularity 
                is daily: weekly seasonality)
        :return: seasonal_markers_dict; dict with keys: timesteps, values: season_index (0:seasonality)
        """

        seasonal_markers_dict = {}
        seasons = range(0,seasonality)
        seasons = seasons/np.max(seasons)
        season_idx = 0
        for ts in timesteps_all:
            seasonal_markers_dict[ts] = seasons[season_idx]
            season_idx+=1
            if season_idx==seasonality: # start from beginning
                season_idx = 0


        return seasonal_markers_dict

    def plot_feature_figure(self, timesteps, timeseries, name, seasonality, dataset_name):
        """ plot timeseries with graph params
            one figure per feature (ie one call of this function per feature)
        """
        plt.figure(figsize=(int(35)/5,int(18/5)))
        plt.plot(timesteps, timeseries, marker='.', markersize=2)
        
        tslist = []
        timeserieslist = []
        for i in range(2, len(timesteps), seasonality):
            tslist.append(timesteps[i])
            timeserieslist.append(timeseries[i])
        plt.scatter(tslist, timeserieslist, s=15.0, label = 'Sundays', color = 'grey', alpha= 0.4)
        min_val = np.min(timeseries) - 0.05*np.median(timeseries)
        max_val = np.max(timeseries) + 0.05*np.median(timeseries)
        plt.vlines(tslist, min_val, max_val, colors='grey', linestyles='solid', label='', alpha = 0.4)
        plt.ylabel(name)
        title_dict = {'Number of Triples': 'a) ', 'Number of Nodes': 'b) ', 'Max Node Degree': 'e) ', 
                      'Mean Node Degree': 'd) ', 'Mean Degree Centrality': None, 'Max Degree Centrality': None, 
                      'Min Degree Centrality': None, 'Density': 'c) '}
        new_name = name
        if name in title_dict.keys():
            if title_dict[name] != None:
                new_name = title_dict[name] +name
            
        plt.title(new_name + ' over Time')

        
        plt.legend()
        
        months = ['Jan', 'Mar',  'May',  'Jul',  'Sep',  'Nov',  'Jan']
        plt.xticks(np.linspace(0,365,7) , months)

        plt.savefig('./figs/' +dataset_name+name+'.pdf')
        print("Stored the analysis figures in ", './figs/' +dataset_name+name+'.pdf')


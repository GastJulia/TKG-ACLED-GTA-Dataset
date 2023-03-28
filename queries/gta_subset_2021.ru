PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX gta: <https://schema.coypu.org/gta#>


DROP GRAPH <https://data.coypu.org/gta/2021/>
;

LOAD <https://gitlab.com/coypu-project/coy-ontology/-/raw/sectors/sectors/data/cpc21_data.ttl> INTO GRAPH <https://data.coypu.org/products/cpc21/>
;

LOAD <https://gitlab.com/coypu-project/coy-ontology/-/raw/sectors/sectors/data/hs2012_data.ttl> INTO GRAPH <https://data.coypu.org/sectors/hs2012/>
;


INSERT {
GRAPH <https://data.coypu.org/gta/2021/> {
  ?a a gta:StateAct ;
   gta:hasAnnouncementDate ?date ;
   gta:hasIntervention ?i .
      
     
  ?i a gta:Intervention ;
        gta:hasAffectedCommercialFlow  ?i_flow ;
        gta:hasGTAEvaluation           ?i_eval ;
        gta:hasImplementationDate      ?i_date ;
        gta:hasImplementationLevel     ?i_level ;
        gta:hasImplementingJurisdiction ?i_jurisdiction ;
        gta:hasInterventionType        ?i_type ;
        gta:hasAffectedSector          ?i_sector ;
        gta:hasAffectedProduct        ?i_product 
   .
}
}
WHERE {
  ?a a gta:StateAct ;
           gta:hasAnnouncementDate ?date ;
           gta:hasIntervention ?i .
        FILTER(year(?date) = 2021) 
     
  ?i a gta:Intervention ;
     gta:hasAffectedCommercialFlow  ?i_flow ;
        gta:hasGTAEvaluation           ?i_eval ;
        gta:hasImplementationDate      ?i_date ;
        gta:hasImplementationLevel     ?i_level ;
        gta:hasImplementingJurisdiction ?i_jurisdiction ;
        gta:hasInterventionType        ?i_type ;
        gta:hasAffectedSector          ?i_sector ;
        gta:hasAffectedProduct        ?i_product 
   .
}
;


# aggregate the products
WITH <https://data.coypu.org/gta/2021/>
DELETE {
?i gta:hasAffectedProduct ?p ;
}
INSERT {
?i gta:hasAffectedProduct ?pp
} WHERE {
       
      ?i a gta:Intervention ;
         gta:hasAffectedProduct ?p .
      GRAPH <https://data.coypu.org/sectors/hs2012/> {?p skos:broader ?pp .}  
};


# aggregate the sectors
WITH <https://data.coypu.org/gta/2021/>
DELETE {
?i gta:hasAffectedSector ?s ;
}
INSERT {
?i gta:hasAffectedSector ?s
} WHERE {
        
      ?i a gta:Intervention ;
         gta:hasAffectedSector ?s .
      GRAPH <https://data.coypu.org/products/cpc21/> {?s skos:broader ?ss . }
};


DROP GRAPH <https://data.coypu.org/sectors/hs2012/>
;

DROP GRAPH <https://data.coypu.org/products/cpc21/>
;

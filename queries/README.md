This directory contains SPARQL `CONSTRUCT` queries and SPARQL Update statements to extract

* year based data
* subset of TKG relevant properties
* aggregated data

based on the corresponding dataset

## ACLED
We provide `CONSTRUCT` queries that can extract the corresponding data from the full ACLED RDF dataset.
The queries can be found in the `acled_*.rq` files:
* [`acled_event_triples_2021.rq`](./acled_event_triples_2021.rq): the event data of year 2021
* [`acled_event_triples_2021_subset.rq`](./acled_event_triples_2021_subset.rq): the event data of year 2021 and only a subset of properties, e.g. identifiers as well as textual properties are omitted 
* [`acled_merged_event_triples_2021_subset.rq`](./acled_merged_event_triples_2021_subset.rq): aggregated ACLED events when 
    * same event type
    * in same country
    * with same participating actors


## GTA
We provide an SPARQL Update statement that 
1) extracts data for year 2021
2) extract only the non-textual properties which are mostly relevant from TKG perspective (e.g. we omit labels and comments)
3) aggregates the affected products and sectors attached to a single intervention such that the higher level products and sectors be used, thus, we have less granularity but also a way smaller dataset
The Update statements can be found in file [`gta_aggregated_sectors_products_2021_subset.ru`](./gta_aggregated_sectors_products_2021_subset.ru) .
It generates a new graph `https://data.coypu.org/gta/2021/` which you can then export.

### Example Usage
We assume Apache Jena being available, otherwise simply load the full GTA RDF data into a triple store of your choice and apply the Update statements as well as export the named graph.
 
#### Load GTA (or you have the existing TDB2 database containg the full GTA RDF dataset)
```bash
tdb2.tdbloader --loc tdb2/gta gta.ttl
```
#### Apply the SPARQL Update statements
```bash
tdb2.tdbupdate --loc tdb2/gta --update gta_aggregated_sectors_products_2021_subset.ru
```

#### Dump the extracted and aggregated graph
```bash
tdb2.tdbquery --loc tdb2/gta "CONSTRUCT {?s ?p ?o} WHERE {GRAPH <https://data.coypu.org/gta/2021/> {?s ?p ?o}}" > gta_2021_aggregated.ttl  
```

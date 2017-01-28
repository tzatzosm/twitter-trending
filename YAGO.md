# [YAGO DB](http://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/yago/downloads/)

## TAXONOMY

### 1. yagoTaxonomy

The entire YAGO taxonomy. These are all rdfs:subClassOf facts derived from multilingual Wikipedia and from WordNet

Sample Triples

    <wordnet_agape_101028534>	rdfs:subClassOf <wordnet_religious_ceremony_101028082>

### 2. yagoTypes

The coherent types extracted from different wikipedias

Sample triples

    <Kayna>	rdf:type	<wikicat_Former_municipalities_in_Saxony-Anhalt> .
    <Kayna>	rdf:type	<wikicat_Towns_in_Saxony-Anhalt> .

### 3. yagoSchema

The domains, ranges and confidence values of YAGO relations

The following predicates are used

    - rdf:type - The subject is an instance of a class.
    - rdfs:domain -  A domain of the subject property. (applies to subject)
    - rdfs:range - A range of the subject property. (applies to object)
    - rdfs:subPropertyOf - The subject is a subproperty of a property.
    - (yago:) hasConfidence - 
    - (yago:) hasGloss - 

### 4. yagoTransitiveType

Transitive closure of all rdf:type/rdfs:subClassOf facts

Sample triples

    <A1086_road>	rdf:type	<wikicat_Roads_in_England> .
    <A1086_road>	rdf:type	<wordnet_artifact_100021939> .
    <A1086_road>	rdf:type	<wordnet_object_100002684> .
    
## CORE
    
### 5. yagoFacts

All facts of YAGO that hold between instances (resources)

Sample triples

    <Wouter_Vrancken>	<playsFor>	<K.V._Kortrijk> .
    <Anthony_Gilbert_(author)>	<diedIn>	<London> .
    <Johan_Jacobsen>	<directed>	<The_Invisible_Army> .

In this samples both subject (left) and object (right) are yago resources.

### 6. yagoLiteralFacts

All facts of YAGO that contain literals (except labels)

Sample triples

    <Gosław,_Opole_Voivodeship>	<hasLongitude>	"18.279722222222222"^^<degrees> .
    <Morgan_County,_Colorado>	<hasLongitude>	"-103.81"^^<degrees> .
    
### 7. yagoLabels

All facts of YAGO that contain labels (rdfs:label, skos:prefLabel, isPreferredMeaningOf, hasGivenName, hasFamilyName, 
hasGloss, redirectedFrom)

Sample triples

    <SIG_MG_710-3>	rdfs:label	"Karabin maszynowy SIG 710-3"@pol .
    <Rouffignac>	rdfs:label	"Rouffignac"@slk .
    <es/Alejandro_Fiore>	rdfs:label	"Alejandro Fiore"@es .

### 8. yagoDateFacts

All facts of YAGO that contain dates

Sample triples 

    <Dirty_Hearts>	<wasCreatedOnDate>	"2011-10-13"^^xsd:date .
    <de/Else_Kienle>	<diedOnDate>	"1970-##-##"^^xsd:date .
    <pl/Erazm_FabijaĹ„ski>	<diedOnDate>	"1892-##-##"^^xsd:date .
    
## MULTILINGUAL

### yagoMultilingualClassLabels

Multi-lingual labels for classes from Universal WordNet

    <wordnet_pear_112651611>	rdfs:label	"dardhë"@aae .
    <wordnet_dictionary_106418901>	rdfs:label	"ажәар"@abk .
    <wordnet_thesaurus_106421016>	rdfs:label	"ажәар"@abk .
    
## LINK

### yagoDBpediaInstances

Mappings of YAGO instances to DBpedia instances 

This can be used to extract additional information about instances from dbbedia.

    <1908_St._Louis_Browns_season>	owl:sameAs	<http://dbpedia.org/resource/1908_St._Louis_Browns_season> .
    <Stathmopoda_aposema>	owl:sameAs	<http://dbpedia.org/resource/Stathmopoda_aposema> .
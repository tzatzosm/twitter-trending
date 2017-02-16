# Twitter Trending

## Content matching against twitter trending topics

The aim of this project is to provide a tool for content owners such as media, museums etc. to retrieve automatically match their content with the twitter trending topics.

[More on yago](YAGO.md)

## Prerequisites to run the project

1. Python 3.+ is required (currently tested on python 3.6, but i think it should be ok on earlier 3+ version)

2. Elastic search instance running http://localhost:9200/ (default)

3. Install the [requirements](requirements.txt) on your virtual env

## For the indexing part you can

```
    from rdflib import URIRef
    from yago_indexer import YagoIndexer

    sites = URIRef("http://yago-knowledge.org/resource/wordnet_site_108651247")

    # The following statement will take some time depending on the size of the files
    # For the current sample files it will take a few seconds
    yi = YagoIndexer(files=[
        'yago_samples/yagoTypesSites.ttl',
        'yago_samples/yagoLabelsSites.ttl',
        'yago_samples/yagoPreferredMeaningsSites.ttl',
        'yago_samples/yagoDBpediaInstancesSites.ttl'])

    # Indexing will take some time since it will have to download some additional info from dbpedia.
    # Data are not downloaded but instead loaded into the graph and queried.
    # As soon as this operation completes you will have all the data indexed into elastic search.
    yi.__index_type__(sites)

```

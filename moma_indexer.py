from datetime import datetime
from elasticsearch import Elasticsearch
from elastic.elastic_manager import ElasticManager

import json

artist_json_filename = "data/moma/Artists.json"
artworks_json_filename = "data/moma/Artworks.json"

class MomaIndexer:
    """ Index for the MOMA dataset (Museum of Modern Arts). Artists & Artworks. """
    index_name = "moma"

    def __init__(self):
        self.elastic_manager = ElasticManager("moma")

    def index_artists(self):
        print("Artworks Indexing started")
        doc_type = "artist"
        with open(artist_json_filename) as artists_data:
            artists_json = json.load(artists_data)
        for artist in artists_json:
            artist_id = artist['ConstituentID']
            self.elastic_manager.index_doc(
                doc_type=doc_type,
                doc_payload=artist,
                doc_id=artist_id)
        print("Artworkds Indexing finished")

    def delete_artists(self):
        doc_type = "artist"
        with open(artist_json_filename) as artists_data:
            artists_json = json.load(artists_data)
        for artist in artists_json:
            artist_id = artist['ConstituentID']
            print(self.elastic_manager.delete_doc(
                doc_type=doc_type,
                doc_id=artist_id))

    def index_artworks(self):
        print("Artworks Indexing started")
        doc_type = "artwork"
        with open(artworks_json_filename) as artworks_data:
            artworks_json = json.load(artworks_data)
        for artwork in artworks_json:
            artwork_id = artwork['ObjectID']
            self.elastic_manager.index(
                doc_type=doc_type,
                doc_payload=artwork,
                doc_id=artwork_id)
        print("Artworks Indexing finished")

# moma_indexer = MomaIndexer()

# moma_indexer.index_artists()
# moma_indexer.index_artworks()

elastic_manager = ElasticManager("moma")

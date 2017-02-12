import json, time
import rdflib

from pprint import pprint

from rdflib import RDFS
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import OWL

from elastic.elastic_manager import ElasticManager



class YagoIndexer:

    ns_yago = "http://yago-knowledge.org/resource/"

    def __init__(self, files):
        self.files = files
        self.em = ElasticManager('yago')
        self.__init_graph__()

    def __init_graph__(self):
        self.graph = rdflib.ConjunctiveGraph()
        # yago taxonomy rdf model

        self.__load_graph_data__()
        # self.__index_by_types__(['wordnet_site_108651247'])


    def __load_graph_data__(self):
        """
        Initializes the graph and loads the data. This function
        will take too much time if run for the original files.

        :param sample:          If true, sample files will be loaded. Default value true.
        """
        start_time = time.time()
        print("Loading data into graph")
        for file in self.files:
            self.__load_file__(file)
        print("Loading data into graph finished after {0}".format((time.time() - start_time)))


    def __load_file__(self, file_path):
        """

        :param file_path:       Path to the file that will be loaded into the graph.
        :param sample:          If true the sample file will be loaded.
        """
        try:
            print("Loading {0}".format(file_path))
            start_time = time.time()
            self.graph.load(file_path, format='n3')
            print("Loading {0}, finished after {1} seconds"
                  .format(file_path, time.time() - start_time))
        except FileNotFoundError:
            from warnings import warn
            warn("File {0} not found.".format(file_path))

    def __get_preferred_meaning__(self, type, lang="eng"):
        """
        Returns preferred meaning for given type if any or None.

        :param type:    (rdflib.URIRef) Type
        :return:        preferred meanings separated by , or None.
        """
        query = prepareQuery(
            """
                SELECT  (group_concat(?prefMeaning;separator=", ") as ?preferredMeanings)
                WHERE {{
                    ?type yago:isPreferredMeaningOf ?prefMeaning .
                    FILTER( LANG(?prefMeaning) = "" || LANGMATCHES(LANG(?prefMeaning), "{0}"))
                }}
            """.format(lang),
            initNs= { 'yago' : self.ns_yago }
        )
        res = self.graph.query(query, initBindings={'type': type})
        if len(res) > 0:
            return list(res)[0]
        return None

    def __get_db_pedia_links__(self, type):
        """
        Queries and returns a list of all subjects of the current type and their dbpedia links.

        :param type:    (rdflib.URIRef) Type
        :return:        List of (subject, dbPediaLink) tuples or None.
        """
        query = prepareQuery(
            """
                SELECT ?subj ?dbPediaLink
                WHERE {
                    ?subj a ?type .
                    ?subj owl:sameAs ?dbPediaLink .
                }
            """,
            initNs={
                'yago' : self.ns_yago,
                'owl' : OWL
            }
        )
        res = self.graph.query(query, initBindings={'type': type})
        if len(res) > 0:
            return list(res)
        return None

    def __get_db_pedia_info__(self, dbpedia_resource, lang="en"):
        """
        DBPedia uses @en for english literals. Inconsistencies everywhere...

        :param dbpedia_resource:
        :param lang:
        :return:
        """
        try:
            dbpedia_uri = self.__get_db_pedia_uri__(dbpedia_resource)
            self.graph.load(dbpedia_uri, format='n3')
            query = prepareQuery(
                """
                    SELECT ?label ?comment
                    WHERE {{
                        ?subj rdfs:label ?label .
                        ?subj rdfs:comment ?comment .
                        FILTER( LANGMATCHES(LANG(?label), "{0}") && LANGMATCHES(LANG(?comment), "{0}"))
                    }}
                """.format(lang),
                initNs= {
                    'rdfs' : RDFS
                }
            )
            res = self.graph.query(query, initBindings={ 'subj': dbpedia_resource })
            if len(res) > 0:
                return list(res)[0]
        except UnicodeEncodeError:
            pass
        return None

    def __get_db_pedia_uri__(self, dbpedia_resource):
        """
        Returns a dbpedia uri that containing the data of the resource defined.

        :param db_pedia_uri_ref:
        :param format:
        :return:
        """
        return "{0}.n3".format(str(dbpedia_resource).replace('/resource/', '/data/'))

    def __index_type__(self, type):
        pref_meaning = self.__get_preferred_meaning__(type)
        dp_pedia_links = self.__get_db_pedia_links__(type)
        for (index, (yago_resource, db_pedia_resource)) in enumerate(dp_pedia_links):
            db_pedia_info = self.__get_db_pedia_info__(db_pedia_resource, 'en')
            if db_pedia_info:
                # print("DBPedia info @ {0} -> {1}, {2}".format(
                #     index, str(db_pedia_info[0]), str(db_pedia_info[1])))
                indexable = self.__get

            else:
                # print("DBPedia info @ {0} -> None".format(index))
                # TODO log error
                pass

    def __get_object_dict__(self, label, comment):
        """
        Returns a new object that can be indexed from elastic search

        :param type:
        :param label:
        :param comment:
        :return:
        """
        return {
            "label": label,
            "comment": comment
        }


    def print_stats(self):
        subjects = list(self.graph.subjects())
        subjects_count = len(subjects)
        print("Total Subjects = {0}".format(subjects_count))

        for subject in subjects:
            print(subject)
            for triple in self.graph.triples((subject,None,None)):
                print("\t{0}".format(triple))

    def print_all(self):
        for (sub, pred, obj) in self.graph:
            print("{0} - {1} - {2}".format(
                self.normalize(sub),
                self.normalize(pred),
                self.normalize(obj)))


    def normalize(self, uri):
        return self.get_last_segment(uri).replace('_', ' ')


    def get_last_segment(self, uri):
        return uri.split('/')[-1]


if __name__ == "__main__":
    yi = YagoIndexer(files=[
        'yago_samples/yagoTypesSites.ttl',
        'yago_samples/yagoLabelsSites.ttl',
        'yago_samples/yagoPreferredMeaningsSites.ttl',
        'yago_samples/yagoDBpediaInstancesSites.ttl'])

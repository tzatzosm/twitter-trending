import json, time
import rdflib

from pprint import pprint

from rdflib import RDFS

from elastic.elastic_manager import ElasticManager

class YagoIndexer:

    yago_types_file_path = 'yago/taxonomy/yagoTypes{0}.ttl'
    yago_taxonomy_file_path = 'yago/taxonomy/yagoTaxonomy{0}.ttl'
    yago_schema_file_path = 'yago/taxonomy/yagoSchema{0}.ttl'

    def __init__(self):
        self.em = ElasticManager('yago')
        self.__init_graph__()

    def __init_graph__(self):
        self.graph = rdflib.Graph()
        # yago taxonomy rdf model

        self.__load_graph_data__()
        self.__index_taxonomy__()
        print(len(self.graph))


    def __load_graph_data__(self, sample=True):
        """
        Initializes the graph and loads the data. This function
        will take too much time if run for the original files.

        :param sample:          If true, sample files will be loaded. Default value true.
        """
        start_time = time.time()
        print("Loading data into graph")
        self.__load_file__(self.yago_types_file_path, sample)
        self.__load_file__(self.yago_taxonomy_file_path, sample)
        self.__load_file__(self.yago_schema_file_path, sample)
        print("Loading data into graph finished after {0}".format((time.time() - start_time)))


    def __load_file__(self, file_path, sample):
        """

        :param file_path:       Path to the file that will be loaded into the graph.
        :param sample:          If true the sample file will be loaded.
        """
        print("Loading {0}, sample : {1}".format(file_path, sample))
        start_time = time.time()
        suffix = 'Sample' if sample else ''
        self.graph.load(file_path.format(suffix), format='n3')
        print("Loading {0}, sample : {1} finished after {2} seconds"
              .format(file_path, sample, time.time() - start_time))


    def __index_taxonomy__(self):
        """
            Indexes all subjects defined in yago taxonomy file.
            The object read will be save at key subClassOf as an object
            with its uri and a friendly name and its id (parsed from the uri as defined in yago) .
        """
        self.data = {}
        for (subject, _, object) in self.graph.triples((None, RDFS.subClassOf, None)):
            # instantiate a new dictionary representing our subject
            subject_uri_string = str(subject)
            subject_dict = self.data.setdefault(subject_uri_string, {})
            subject_dict.setdefault('uri', subject_uri_string)
            # extract name from the subject's uri and set it as the name property of our subclass
            full_name = self.get_last_segment(subject_uri_string)
            subject_dict.setdefault('full_name', full_name)
            # extract category, name and id from the full_name
            # and add them as subject's properties
            name_info = self.get_source_name_id(full_name)
            subject_dict.setdefault('category', name_info[0])
            subject_dict.setdefault('name', name_info[1])
            subject_dict.setdefault('id', name_info[2])

            # define a property named subclass subClassOf for our subject
            subclass = subject_dict.setdefault('_subClassOf', {})
            object_uri_string = str(object)
            subclass.setdefault('uri', object_uri_string)
            # extract name from object's uri and set it as the name property of our subclass
            subclass_name = self.get_last_segment(object_uri_string)
            subclass.setdefault('full_name', subclass_name)
            # extract category, name and id from the full_name
            # and add them as subject's properties
            subclass_name_info = self.get_source_name_id(subclass_name)
            subclass.setdefault('category', subclass_name_info[0])
            subclass.setdefault('name', subclass_name_info[1])
            subclass.setdefault('id', subclass_name_info[2])

            self.em.index_doc('yago', subject_dict)

        # pprint(self.data)

    def get_source_name_id(self, full_name):
        result = (None, None, None)
        tokens = full_name.split('_')
        # Category is set here
        category = tokens[0]

        # TODO cleanup a bit this code...

        # Name ranges from seconds argument to the last-1
        if len(tokens) > 1:
            # if tokens[2] isdigit (meaning is numbers only)
            # we asume it is the id and we join the name till
            # last - 1 (reduce by holds that value)
            reduce_by = 1 if (len(tokens) > 2 and tokens[-1].isdigit()) else 0
            name = "_".join(tokens[1:(len(tokens)-reduce_by)])
        else:
            name = None

        if len(tokens) > 2:
            identifier = tokens[-1]
        else:
            identifier = None

        return (category, name, identifier)


    def __init_dict__(self):
        self.dict = {}
        for (subject, predicate, obj) in self.graph:
            subject_id = self.get_last_segment(subject)
            data = self.dict.setdefault(subject_id, {})
            data.setdefault('name', self.normalize(subject))
            data.setdefault(self.normalize(predicate), self.normalize(obj))


    def save_dict(self):
        with open('data.json', 'w') as fp:
            json.dump(self.dict, fp)


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
    yi = YagoIndexer()

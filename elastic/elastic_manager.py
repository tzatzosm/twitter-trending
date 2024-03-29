from datetime import datetime
from elasticsearch import Elasticsearch

class ElasticManager():
    """
        Helper class responsible for creating, updating
        and quering a single index of the es. A single connection is used.
    """

    def __init__(self, index_name, host='localhost', port='9200'):
        """
            :param host: (string) hostname of the node (default 'localhost')
            :param port: (string) port of the node (default '9200')
            :param index_name: (string) name of the index this class will create
                             (if does not exist), update and query data
        """
        self.index_name = index_name
        self.__init_es__(host, port);

    # TODO make the term vector part more generic
    def __init_es__(self, host, port):
        """ Initializes the connection to the elastic search instance.

            :param host: hostname of the node
            :param port: port of the node
        """
        self.es = Elasticsearch(hosts=self.get_hosts(host, port))
        # create an index with the given name.
        # ignore 400 caused by IndexAlreadyExistsException when creating an index
        self.es.indices.create(
            index=self.index_name,
            ignore=400)

    def get_hosts(self, host, port):
        """ Returns the host string wrapped in a python array
            as required by es python constructor. """
        return ["{0}:{1}".format(host, port)]

    def get_doc(self, doc_type, doc_id, default=None):
        """ Returns a document (inside the index specified during initialization) by its id,
            if exists one or default.

            :param doc_type:		type of the document
            :param doc_id:        document id
            :return:            document found.
		"""
        doc = self.es.get(index=self.index_name, doc_type=doc_type, id=doc_id)
        if doc['found']:
            return doc['_source']
        return None

    def index_doc(self, doc_type, doc_payload, doc_id=None):
        """ Index (create or update) a document in the index specified during initialization.

            :param doc_type:      type of the document to index
            :param doc_payload:   json object containing the document data
            :param doc_id:        document id, if not specified es will generate one (default=None)
            :param parent_id:     parent document id (default=None)
            :return:            json result of the action as returned by the es python library
        """
        return self.es.index(
            index=self.index_name,
            doc_type=doc_type,
            body=doc_payload,
            id=doc_id)

    def delete_doc(self, doc_type, doc_id):
        """ Delete (create or update) a document in the index specified during initialization.

            :param doc_type:      type of the document to index
            :param doc_id:        document id, if not specified es will generate one (default=None)
            :param parent_id:     parent document id (default=None)
            :return:            json result of the action as returned by the es python library
        """
        return self.es.delete(
            index=self.index_name,
            doc_type=doc_type,
            id=doc_id)


    def upsert_props(self, doc_type, doc_id, props):
        """ Insert or update properties for the a document.

            :param doc_type:      type of the document
            :param doc_id:        document id
            :param props:         dictionary with the additional properties that will be either inserted or updated
            :return:            json result of the index action as return by the es python library
        """
        doc = self.get_doc(doc_type=doc_type, doc_id=doc_id)
        doc.update(props)
        self.index_doc(doc_type=doc_type, doc_payload=doc, doc_id=doc_id)

    def remove_props(self, doc_type, doc_id, props):
        """ Delete properties for the a document.

            :param doc_type:      type of the document
            :param doc_id:        document id
            :param props:         list with the properties that will be removed from the object
            :return:            json result of the index action as return by the es python library
        """
        doc = self.get_doc(doc_type=doc_type, doc_id=doc_id)
        for key in props:
            if key in doc:
                del doc[key]
        self.index_doc(doc_type=doc_type, doc_payload=doc, doc_id=doc_id)

from __future__ import division, print_function

# built-in libraries
import logging
import os
import pymongo
import re
import warnings

import json
import sys
from bson import ObjectId

class Dataset(object):
    def __init__(self, mongo_db_name, mongo_collection_name, owner_id=None):

        """Class that contains methods to interact with a database
          mongo_db_name(str): database name
          mongo_collection_name(str): collection name
          merged_vcf_path(str): path to merged vcf
        """
        self._mongo_db_name = mongo_db_name
        self._mongo_collection_name = mongo_collection_name
        #self._json_file_path = json_file_path
        self._owner_id = owner_id

        self._mongo_client = pymongo.MongoClient(maxPoolSize=None, waitQueueTimeoutMS=200)
        self._mongo_db = getattr(self._mongo_client, self._mongo_db_name)
        self._mongo_db_collection = getattr(self._mongo_db, self._mongo_collection_name)

    @property
    def full_name(self):
        """Full name of database and collection

        Args:

        Returns:
          str: Full name of database and collection

        """

        return self._mongo_db_collection.full_name

    @property
    def is_empty(self):
        """If there are no records in the collection, returns True

        Args:

        Returns:
          bool: if there are no records in the collection, returns True

        """

        return self._mongo_db_collection.count() == 0

    @property
    def num_records(self):
        """Number of records in MongoDB collection

        Args:

        Returns:
          int: Number of records in MongoDB collection

        """

        return self._mongo_db_collection.count_documents({})
    
    def get_custom_filtered_data(self, filter_dictionary):
      if self.is_empty:
        warnings.warn("Dataset '{0}' is empty, so all filters return an empty list.".format(self.full_name))
      return list(self._mongo_db_collection.find(filter_dictionary))



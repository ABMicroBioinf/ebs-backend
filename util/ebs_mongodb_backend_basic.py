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
import urllib.parse
import csv
import pprint
class GenomeDataset(object):
    def __init__(self, mongo_db_name, mongo_collection_name, json_file_path=None, owner_id=None):

        """Class that contains methods to interact with a parsed database of variants
        Args:
          mongo_db_name(str): database name
          mongo_collection_name(str): collection name
          merged_vcf_path(str): path to merged vcf
        """
        self._mongo_db_name = mongo_db_name
        self._mongo_collection_name = mongo_collection_name
        self._json_file_path = json_file_path
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

    def parse_assembly_stats(self, filePath):

      with open(filePath) as file:
          reader = csv.DictReader(file, delimiter="\t")
          data = list(reader)
          mydict = data[0]
          del mydict["Name"]
          del mydict["ok"]
          mydict["count"] = mydict["no"]
          del mydict["no"]
      return mydict

    def parse_virulome(self, filePath):
        jsonStr = ""
        pp = pprint.PrettyPrinter(indent=4)
        with open(filePath) as file:
            reader = csv.DictReader(file, delimiter="\t")
            mylist = list(reader)
            lowcase_key_list = []
            for data in mylist:
                del data['#FILE']
                data['PCT_COVERAGE'] = data['%COVERAGE']
                del data['%COVERAGE']
                data['PCT_identity'] = data['%IDENTITY']
                del data['%IDENTITY']
                new_data = dict((k.lower(), v) for k, v in data .items()) 
                lowcase_key_list.append(new_data)
        return lowcase_key_list

    def parse_amr(self, filePath):
        jsonStr = ""
        pp = pprint.PrettyPrinter(indent=4)
        with open(filePath) as file:
            reader = csv.DictReader(file, delimiter="\t")
            mylist = list(reader)
            lowcase_key_list = []
            for data in mylist:
                del data['#FILE']
                data['PCT_COVERAGE'] = data['%COVERAGE']
                del data['%COVERAGE']
                data['PCT_identity'] = data['%IDENTITY']
                del data['%IDENTITY']
                new_data = dict((k.lower(), v) for k, v in data .items()) 
                lowcase_key_list.append(new_data)
        return lowcase_key_list
        

    def parse_gff(self):
        filePath = "SRR1162491/contigs.gff"
        records = []
        data = {}
        result = []
        with open(filePath) as file:
            for line in file.readlines():
                if line[0] == '#':
                    continue
                elif line[0] == '##FASTA' or re.findall("^>", line[0]):
                    break
                segment = re.split('\t| ', line)
                #print(len(segment))
                if(len(segment) == 1):
                    print(segment)

                #print(segment)
                attributesString = re.split('\n|;', segment[8])
                #attributes = {}
                attributes = []
                id = ""
                for s in attributesString:
                    e = s.split('=')
                    tv = {}
                    if len(e) >= 2 :
                        tv["tag"] = e[0]
                        tv["value"] = urllib.parse.unquote(e[1])
                        attributes.append(tv)
                        if e[0] == "ID":
                          id = e[1]
                
                record = {
                    
                    'seqName': segment[0],
                    'source': segment[1],
                    'feature': segment[2],
                    'start': int(segment[3])-1,
                    'end': int(segment[4]),
                    'score': segment[5],
                    'strand': segment[6],
                    'frame': segment[7],
                    'attribute': attributes,
                    }
                records.append(record)
        data["gff"] = records
        data['owner_id'] = ObjectId(self._owner_id)
        data['id'] = "SRR1162491"
        print(type(data))
        result.append(data)
        try:
          self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
          self._mongo_db_collection.insert_many(result)
          return "loading gff True"
        except Exception as e:
          print("load gff An exception occurred ::", e)
          return "loading gff False"
  
        #return records

    def load_jsons(self):
      """
      load the all the json files in the give path to the database
      """
      import pprint
      result = []
      data = {}
      output = self.parse_assembly_stats("SRR1162491/contigs.summary.tab")
      pp = pprint.PrettyPrinter(indent=4)
      # pp.pprint(output)
      # print(type(output))
      data["assembly_stats"] = output
      virulome_list = self.parse_virulome("SRR1162491/virulome.tab")
      #print(virulome_list)
      data["virulome"] = virulome_list
      data["amr"] = self.parse_amr("SRR1162491/resistome.tab")
      
      data['owner_id'] = ObjectId(self._owner_id)
      data['annotation_id'] = "SRR1162491"
      result.append(data)
      #result.append(virulome_list)
      #print(json.dumps(result))
      
      try:
        self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
        self._mongo_db_collection.insert_many(result)
        return "loading json True"
      except Exception as e:
        print("An exception occurred ::", e)
        return "Loading json False"
  
    
    def get_custom_filtered_data(self, filter_dictionary):
      if self.is_empty:
        warnings.warn("Dataset '{0}' is empty, so all filters return an empty list.".format(self.full_name))
      return list(self._mongo_db_collection.find(filter_dictionary))

    

def main():
  
  genome_dataset = GenomeDataset("ebsdb", "genome_genome","/home/xdong/deve/ebs-backend/util", "60d4dfba7109403cf2d20636")
 # genome_dataset = GenomeDataset("test", "genome","/home/xdong/deve/ebs-backend/util" , "60d4dfba7109403cf2d20636")
  count = genome_dataset.num_records
  full_name = genome_dataset.full_name
  
  print(full_name + " collection is having " + str(count) + " records", file=sys.stderr)

  #return list of dictionary
  print(genome_dataset.load_jsons())
  annotation_dataset = GenomeDataset("ebsdb", "genome_annotation","/home/xdong/deve/ebs-backend/util", "60d4dfba7109403cf2d20636")
  print(annotation_dataset.parse_gff())


  pass


if __name__ == '__main__':
  main()


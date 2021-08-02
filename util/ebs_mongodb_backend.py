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

class TBDataset(object):
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

    def load_jsons(self):
      """
      load the all the json files in the give path to the database
      """
      import pprint
      result = []
      for f_name in os.listdir(self._json_file_path):
        if f_name.endswith('.json'):
          print(f_name)

          with open(f_name) as f:
            jsonData = json.load(f)

          data = {}
          resist = {}
          
          



          tmp_drugs = ["rifampicin", "isoniazid", "pyrazinamide", "ethambutol", "streptomycin", "fluoroquinolones", "moxifloxacin", "ofloxacin", "levofloxacin", "ciprofloxacin", "aminoglycosides", "amikacin", "kanamycin", "capreomycin", "ethionamide", "para-aminosalicylic_acid", "cycloserine", "linezolid"]

          for key, value in jsonData.items():
            if key not in {"qc", "delly"}:
              #print({key: value})
              #print(type({key: value}))
              #data[key] = value
              data[key.lower()] = value
              if key == "dr_variants":
                data["num_dr_variants"] = len(value)
                for x in value:
                  l = x['drugs']
                  gene = x["gene"]
                  change = x["change"]
                  
                  freq = x["freq"]
                  print(type(l))
                  print(len(l))
                  for y in l:
                    drug = y["drug"]
                    print(drug + "" + gene + " " + change + "(" + str(freq) + ")" + "\"")
                    resist[drug] = resist.get(drug, "") + gene + " " + change + ";"
                    
              elif key == "other_variants":
                data["num_other_variants"] = len(value)
            elif key == "qc":
              for qkey, qvalue in value.items():
                if qkey in {"pct_reads_mapped", "num_reads_mapped"}:
                  data[qkey.lower()] = qvalue
          
          # for d in tmp_drugs:
          #   if d not in resist:
          #     resist[d] = "-"
          #     pass
          resist_result = []
          for k, v in resist.items():
            resist_result.append({'drug': k, 'mutations': v})

          print(json.dumps(resist_result))

          pp = pprint.PrettyPrinter(indent=4)
          pp.pprint(resist)
          #data["dr_resistances"] = resist
          data["dr_resistances"] = resist_result
          
          data['owner_id'] = ObjectId(self._owner_id)
          result.append(data)
          pp.pprint(data)
      print(type(result))
      #return result
      try:
        self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
        self._mongo_db_collection.insert_many(result)
        return True
      except Exception as e:
        print("An exception occurred ::", e)
        return False
  
    def get_resistance_report(self):
      return ""

    def get_custom_filtered_data(self, filter_dictionary):
      if self.is_empty:
        warnings.warn("Dataset '{0}' is empty, so all filters return an empty list.".format(self.full_name))
      return list(self._mongo_db_collection.find(filter_dictionary))



def main():
  
  tb_dataset = TBDataset("ebsdb", "tb_profile","/home/xdong/deve/ebs-backend/util", "60d4dfba7109403cf2d20636")
  #tb_dataset = TBDataset("test", "my_tb_profile","/home/xdong/deve/ebs-backend/util", "60d4dfba7109403cf2d20636")
  count = tb_dataset.num_records
  full_name = tb_dataset.full_name
  
  print(full_name + " collection is having " + str(count) + " records", file=sys.stderr)

  #return list of dictionary
  print(tb_dataset.load_jsons())
  

  pass


if __name__ == '__main__':
  main()


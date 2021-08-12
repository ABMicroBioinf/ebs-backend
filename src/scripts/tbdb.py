from ebsdb import Dataset
import pprint
import csv
import pymongo
from bson import ObjectId
import dateutil.parser
from datetime import datetime
import os
import json

class TBDataset(Dataset):

    def add2collection_profile_parse_json(self, dir):
      """
      load the all the json files in the give path to the database
      """
      tb_drugs = [
      "rifampicin",
      "isoniazid",
      "pyrazinamide",
      "ethambutol",
      "streptomycin",
      "fluoroquinolones",
      "moxifloxacin",
      "ofloxacin",
      "levofloxacin",
      "ciprofloxacin",
      "aminoglycosides",
      "amikacin",
      "kanamycin",
      "capreomycin",
      "ethionamide",
      "para_aminosalicylic_acid",
      "cycloserine",
      "linezolid",
      "bedaquiline",
      "clofazimine",
      "delamanid"
      ]
    
      result = []
      for filename in os.listdir(dir):
        if not filename.endswith('.json'):
          continue
        else:
          
          print(filename)
          
          with open(os.path.join(dir, filename)) as f:
            data = {}
            resist = {}
            id = os.path.splitext(filename)[0]
            data['id'] = id
            data['Description'] = ""
            data['owner_id'] = ObjectId(self._owner_id)
            data['DateCreated'] = datetime.now()
            data['LastUpdate'] = datetime.now()
          
            jsonData = json.load(f)
            for key, value in jsonData.items():
              if key not in {"qc", "delly"}:
                #print({key: value})
                #print(type({key: value}))
                #data[key] = value
                data[key] = value
                if key == "dr_variants":
                  data["num_dr_variants"] = len(value)
                  for x in value:
                    l = x['drugs']
                    gene = x["gene"]
                    change = x["change"]
                    
                    freq = x["freq"]
                    
                    for y in l:
                      drug = y["drug"]
                      drug_no_hyphen = drug.replace("-", "_")
                      #print(drug + "" + gene + " " + change + "(" + str(freq) + ")" + "\"")
                      resist[drug_no_hyphen] = resist.get(drug_no_hyphen, "") + gene + " " + change + ";"
                elif key == "other_variants":
                  data["num_other_variants"] = len(value)
              elif key == "qc":
                for qkey, qvalue in value.items():
                  if qkey in {"pct_reads_mapped", "num_reads_mapped"}:
                    data[qkey] = qvalue
            
            for d in tb_drugs:
              if d not in resist:
                resist[d] = "-"

            resist_result = []
            for k, v in resist.items():
              resist_result.append({'drug': k, 'mutations': v})
            data["dr_resistances"] = resist_result
            result.append(data)
           
            
      try:
        self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
        self._mongo_db_collection.insert_many(result)
        return "adding tbprofile json data success"
      except Exception as e:
        print("An exception occurred ::", e)
        return "adding tbprofile json data failed"

    def add2collection_sumary_parse_json(self, dir):
      """
      load the all the json files in the give path to the database
      """
      tb_drugs = [
      "rifampicin",
      "isoniazid",
      "pyrazinamide",
      "ethambutol",
      "streptomycin",
      "fluoroquinolones",
      "moxifloxacin",
      "ofloxacin",
      "levofloxacin",
      "ciprofloxacin",
      "aminoglycosides",
      "amikacin",
      "kanamycin",
      "capreomycin",
      "ethionamide",
      "para_aminosalicylic_acid",
      "cycloserine",
      "linezolid",
      "bedaquiline",
      "clofazimine",
      "delamanid"
      ]
    
      result = []
      for filename in os.listdir(dir):
        if not filename.endswith('.json'):
          continue
        else:
          
          print(filename)
          
          with open(os.path.join(dir, filename)) as f:
            data = {}
            resist = {}
            id = os.path.splitext(filename)[0]
            data['id'] = id
            data['Description'] = ""
            data['owner_id'] = ObjectId(self._owner_id)
            data['DateCreated'] = datetime.now()
            data['LastUpdate'] = datetime.now()
          
            jsonData = json.load(f)
            for key, value in jsonData.items():
              if key not in {"qc", "delly", "lineage", "dr_variants","other_variants", "pipeline", "db_version",  "tbprofiler_version", "timestamp"}:
                data[key] = value
                
              elif key == "dr_variants":
                data["num_dr_variants"] = len(value)
                for x in value:
                  l = x['drugs']
                  gene = x["gene"]
                  change = x["change"]
                  
                  freq = x["freq"]
                  
                  for y in l:
                    drug = y["drug"]
                    #print(drug + "" + gene + " " + change + "(" + str(freq) + ")" + "\"")
                    drug_no_hyphen = drug.replace("-", "_")
                      #print(drug + "" + gene + " " + change + "(" + str(freq) + ")" + "\"")
                    resist[drug_no_hyphen] = resist.get(drug_no_hyphen, "") + gene + " " + change + ";"
                    
              elif key == "other_variants":
                data["num_other_variants"] = len(value)
              elif key == "qc":
                for qkey, qvalue in value.items():
                  if qkey in {"pct_reads_mapped", "num_reads_mapped"}:
                    data[qkey] = qvalue
              
            
            for d in tb_drugs:
              if d not in resist:
                resist[d] = "-"

            resist_result = []
            for k, v in resist.items():
              resist_result.append({'drug': k, 'mutations': v})
              data[k] = v
            result.append(data)
      try:
        self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
        self._mongo_db_collection.insert_many(result)
        return "adding tbprofile json data success"
      except Exception as e:
        print("An exception occurred ::", e)
        return "adding tbprofile json data failed"

def main():
  profile = TBDataset("ebsdb", "tb_profile_full", "60d4dfba7109403cf2d20636")
  profile.add2collection_profile_parse_json("data/tbprofiler/results")
  summary = TBDataset("ebsdb", "tb_profile", "60d4dfba7109403cf2d20636")
  summary.add2collection_sumary_parse_json("data/tbprofiler/results")
  

if __name__ == '__main__':
  main()


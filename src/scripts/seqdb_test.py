from ebsdb import Dataset
import pprint
import csv
import pymongo
from bson import ObjectId
import dateutil.parser
from datetime import datetime
import os
import re
import xml.etree.ElementTree as ET

class Seq(Dataset):

    def parse_seqstats(self, filePath, newkey, sep):
        
        pp = pprint.PrettyPrinter(indent=4)
        with open(filePath) as file:
            reader = csv.DictReader(file, delimiter=sep)
            list_seqstats = list(reader)
            print(list_seqstats)
            for rowindex, row in enumerate(list_seqstats):
                #seqid = row['Seqfile']
                seqid = row['Isolate']
                #del row['seqtype']
                #del row['Seqfile']
                del row['Isolate']
                print("******************************")
                print(type(row))
                newrow = {}
                for key, value in row.items():
                    # print("(((((((((((((((((((((((((((((((((((((((((((((((((((((")
                    # print(key)
                    # print(value)
                    try:
                        newrow[key] = int(value)
                    except ValueError:
                        newrow[key] = float(value)

                try:
                    self._mongo_db_collection.update_one({"id": seqid}, {"$set": {newkey: newrow }})
                    
                    #return "updated sequence collection True"
                except Exception as e:
                    print("An exception occurred ::", e)
                    return "parse_seqstats " + filePath + " failed"

        return list_seqstats
    
    def add2seq_stat(self, rawStatFilePath, qcStatFilePath, sep):
        """
        add new entries into the genome collection
        
        Sample_id       CDS     CRISPR  ncRNA   oriC    rRNA    region  regulatory_region       tRNA    tmRNA
        ERR1679637      4160    3       19      2       3       449     13      46      1
        """
        
        results = {}
        with open(rawStatFilePath) as rfile:
            reader = csv.DictReader(rfile, delimiter=sep)
            list_stats = list(reader)
            newrow = {}
            for rowindex, row in enumerate(list_stats):
                id = row['Isolate']
                del row['Isolate']
                newrow['id'] = id
                #print(row)
                for x in row:
                    try:
                        newrow['r_' + x] = int(row[x])
                    except ValueError:
                        newrow['r_' + x] = float(row[x])
                
                
                results[id]= newrow
                print("**********************=" + id, end='\n')
                print(results[id], end='\n')
            #print(list_stats, end='\n')
           
            
        with open(qcStatFilePath) as qfile:
            reader = csv.DictReader(qfile, delimiter=sep)
            list_stats = list(reader)
            newrow = {}
            for rowindex, row in enumerate(list_stats):
                id = row['Isolate']
                del row['Isolate']
                newrow['id'] = id
                #print(row)
                #newrow['qid'] = id
                for x in row:
                    try:
                        newrow['q_' + x] = int(row[x])
                    except ValueError:
                        newrow['q_' + x] = float(row[x])
                
                results[id] = dict(results[id], **newrow)

            #print(list_stats, end='\n')
            print(results.values())
            """ for key, value in results.items():
                print(key, '->', value) """
            try: 
                self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
                self._mongo_db_collection.insert_many(results.values())
                return "add2seq_seqstat: " + rawStatFilePath + ', ' + qcStatFilePath+ " success"
            except Exception as e:
                print("An exception occurred ::", e)
                return "add2seq_seqstat: " + rawStatFilePath + ', ' + qcStatFilePath+  " failed"

    def parse_runinfo(self, filePath, type):
        
        #column id of the selected metadata downloaded using esearch
        selected_fileds = (
            "BioProject", 
            "SampleName", 
            "CenterName",
            "ScientificName",
            "TaxID",
            "Run", 
            # "avgLength", 
            # "bases", 
            # "spots", 
            # "size_MB", 
            "Experiment", 
            "Platform", 
            "LibraryName",
            #"InsertSize", 
            #"InsertDev", 
            "LibrarySelection", 
            "Model", 
            "LibraryStrategy", 
            "LibraryLayout", 
            "LibrarySource", 
            "ReleaseDate"
        )
        pp = pprint.PrettyPrinter(indent=4)
        with open(filePath) as file:
            reader = csv.DictReader(file, delimiter=",")
            list_runinfo = list(reader)
            for rowindex, row in enumerate(list_runinfo):
                
                for key, value in row.copy().items():
                    
                    if (key not in selected_fileds):
                        del row[key]

                row['owner_id'] = ObjectId(self._owner_id)
                row['project_id'] = row.pop('BioProject')
                
                row['SequencerModel'] = row.pop('Model')
                row['DateCreated'] = dateutil.parser.parse(row.pop('ReleaseDate'))
                row['id'] = row.pop('Run')
                row['assembly_id'] = row['id']
                row['seqtype'] = type
                row['LastUpdate'] = datetime.now()
                row['Description'] = ""
                row['TaxID'] = int(row['TaxID'])

            #print(list_runinfo)
        
        try: 
            self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
            self._mongo_db_collection.insert_many(list_runinfo)
            return "loading json True"
        except Exception as e:
            print("An exception occurred ::", e)
            return "parse_runinfo: " + filePath + " failed"
        return list_runinfo

    def parse_bracken_output(self, dir):

        #ERR036228.bracken.output.txt
        for filename in os.listdir(dir):
            data = {}
            if filename.endswith("_bracken.output.txt"): 
                print(filename)
                #fname = ntpath.basename(filename)
                prefix = filename.split(os.extsep)[0]
                id = prefix.replace('_bracken', '')
                data['id'] = id
                print("***********************=" + id)
                file = os.path.join(dir, filename)
                with open(file) as f:
                    next(f)
                    i = 0
                    for line in f:
                        row = line.rstrip()
                        segment = re.split('\t', row)
                        print(line)
                        i += 1
                        data["taxName_" + str(i)] = segment[0]
                        data["taxFrac_" + str(i)] = float(segment[-1])

                        if i >= 4:
                            break
                data['LastUpdate'] = datetime.now()

                try:
                    self._mongo_db_collection.update_one({"id": id}, {"$set": data})
                    #return "updated sequence collection True"
                except Exception as e:
                    print("An exception occurred ::", e)
                    return "parse_braken " + dir + " failed"

        return "success"

def main():
  
    seqstat = Seq("ebsdb", "seq_stat", "60d4dfba7109403cf2d20636")
    seqstat.add2seq_stat("data/cpo/PRJNA725227/Report/short_reads_raw_seqstats.tsv", "data/cpo/PRJNA725227/Report/short_reads_qc_seqstats.tsv", "\t")
    
    

if __name__ == '__main__':
  main()

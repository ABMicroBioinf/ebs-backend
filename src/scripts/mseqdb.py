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

    def add2seq_stat(self, rawStatFilePath, qcStatFilePath, sep):
        """
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
                
                newrow['owner_id'] = ObjectId(self._owner_id)
                results[id]= newrow
                #print("**********************=" + id, end='\n')
                #print(results[id], end='\n')
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
            #print(results.values())
            """ for key, value in results.items():
                print(key, '->', value) """
            try: 
                self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
                self._mongo_db_collection.insert_many(results.values())
                return "add2seq_seqstat: " + rawStatFilePath + ', ' + qcStatFilePath+ " success"
            except Exception as e:
                print("An exception occurred ::", e)
                return "add2seq_seqstat: " + rawStatFilePath + ', ' + qcStatFilePath+  " failed"
            
   
    def add2seq_biosample(self, filePath, sampleType):
        #column id of the selected metadata downloaded using esearch
        selected_fileds = (
            "BioProject", 
            "BioSample",
            "ScientificName",
             "ReleaseDate"
        )
        
        """ >>> lod = [{1: "a"}, {2: "b"}]
        >>> any(1 in d for d in lod)
        True
        >>> any(3 in d for d in lod)
        False """
        
        pp = pprint.PrettyPrinter(indent=4)
        with open(filePath) as file:
            reader = csv.DictReader(file, delimiter=",")
            list_runinfo = list(reader)
            mylist = []
            for rowindex, row in enumerate(list_runinfo):
                
               
                for key, value in row.copy().items():
                    
                    if (key not in selected_fileds):
                        del row[key]
                #print(row)
                row['owner_id'] = ObjectId(self._owner_id)
                row['project_id'] = row.pop('BioProject')
                row['id'] = row.pop('BioSample')
                row['DateCreated'] = dateutil.parser.parse(row.pop('ReleaseDate'))
                row['sampleType'] = sampleType
                row['LastUpdate'] = datetime.now()
                row['Description'] = ""
                 #delete duplicate biosample items
                # for d in list_runinfo:
                #     print(d)
                if not any(d['id'] == row['id'] for d in mylist):
                    mylist.append(row)
                
            #print(mylist)
        
        try: 
            self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
            self._mongo_db_collection.insert_many(mylist)
            return "loading json True"
        except Exception as e:
            print("An exception occurred ::", e)
            return "parse_runinfo: " + filePath + " failed"
        return mylist
    
    def add2seq_sequence(self, filePath, sampleType):
        #column id of the selected metadata downloaded using esearch
        selected_fileds = (
            "BioProject", 
            "BioSample",
            #"SampleName", 
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
                row['biosample_id'] = row.pop('BioSample')
                row['SequencerModel'] = row.pop('Model')
                row['DateCreated'] = dateutil.parser.parse(row.pop('ReleaseDate'))
                row['id'] = row.pop('Run')
                row['assembly_id'] = row['id']
                row['sampleType'] = sampleType
                row['LastUpdate'] = datetime.now()
                row['Description'] = ""
                row['TaxID'] = int(row['TaxID'])
                row['seqstat_id'] = row['id']
            #print(list_runinfo)
        
        try: 
            self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
            self._mongo_db_collection.insert_many(list_runinfo)
            return "loading json True"
        except Exception as e:
            print("An exception occurred ::", e)
            return "parse_runinfo: " + filePath + " failed"
        return list_runinfo
    
    
    def update2seq_sequence_with_bracken_output(self, dir):

        #ERR036228.bracken.output.txt
        for filename in os.listdir(dir):
            data = {}
            if filename.endswith("_bracken.output.txt"): 
                #print(filename)
                #fname = ntpath.basename(filename)
                prefix = filename.split(os.extsep)[0]
                id = prefix.replace('_bracken', '')
                data['id'] = id
                #print("***********************=" + id)
                file = os.path.join(dir, filename)
                with open(file) as f:
                    next(f)
                    i = 0
                    for line in f:
                        row = line.rstrip()
                        segment = re.split('\t', row)
                        #print(line)
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
  
    sequence = Seq("ebsdb", "mseq_sequence", "60d4dfba7109403cf2d20636")
    seqstat = Seq("ebsdb", "mseq_seqstat", "60d4dfba7109403cf2d20636")
    biosample = Seq("ebsdb", "mseq_biosample", "60d4dfba7109403cf2d20636")
   
    # biosample.add2seq_biosample("data/mg/PRJNA234451/PRJNA234451_SraRunInfo.csv", "MG")
    # biosample.add2seq_biosample("data/mg/PRJNA257543/PRJNA257543_SraRunInfo.csv", "MG")
    # biosample.add2seq_biosample("data/mg/PRJNA516442/mg_PRJNA516442_SraRunTable.csv", "MG")
    # biosample.add2seq_biosample("data/mg/PRJNA558701/mg_PRJNA558701_nanopore_SraRunInfo.csv", "MG")
    biosample.add2seq_biosample("data/mg/PRJNA558701/mg_PRJNA558701_illumina_SraRunInfo.csv", "MG")
    
    # sequence.add2seq_sequence("data/mg/PRJNA234451/PRJNA234451_SraRunInfo.csv", "MG")
    # sequence.add2seq_sequence("data/mg/PRJNA257543/PRJNA257543_SraRunInfo.csv", "MG")
    # sequence.add2seq_sequence("data/mg/PRJNA516442/mg_PRJNA516442_SraRunTable.csv", "MG")
    # sequence.add2seq_sequence("data/mg/PRJNA558701/mg_PRJNA558701_nanopore_SraRunInfo.csv", "MG")
    
    # seqstat.add2seq_stat("data/mg/PRJNA234451/report/short_reads_raw_seqstats.tsv", "data/mg/PRJNA234451/report/short_reads_dehost_seqstats.tsv","\t")
    # seqstat.add2seq_stat("data/mg/PRJNA257543/report/short_reads_raw_seqstats.tsv", "data/mg/PRJNA257543/report/short_reads_dehost_seqstats.tsv","\t")
    # seqstat.add2seq_stat("data/mg/PRJNA516442/report/short_reads_raw_seqstats.tsv", "data/mg/PRJNA516442/report/short_reads_dehost_seqstats.tsv","\t")
    # seqstat.add2seq_stat("data/mg/PRJNA558701/illumina/report/short_reads_raw_seqstats.tsv", "data/mg/PRJNA558701/illumina/report/short_reads_dehost_seqstats.tsv","\t")
    # seqstat.add2seq_stat("data/mg/PRJNA558701/nanopore/report/long_reads_raw_seqstats.tsv", "data/mg/PRJNA558701/nanopore/report/long_reads_dehost_seqstats.tsv","\t")
    
   
if __name__ == '__main__':
  main()

from ebsdb import Dataset
import pprint
import csv
import pymongo
from bson import ObjectId
import dateutil.parser
from datetime import datetime
import ntpath
import os
import re
import urllib

class GbaseDataset(Dataset):
    

    def add2collection_denovo_tab(self, filePath, seqtype):
        """
        add new entries into the genome collection
        """
        with open(filePath) as file:
            reader = csv.DictReader(file, delimiter="\t")
            list_contig_stats = list(reader)
            #ERR036228/contigs.fa    177     4254254 4252920 1334    0       213     24035       180126  80234
            for rowindex, row in enumerate(list_contig_stats):
                id = row['Name'].split("/")[0]
                del row['Name']
                row['count'] = row.pop('no')
                del row['ok']
                for x in row:
                    row[x] = int(row[x])

                row['id'] = id
                #row['genome_id'] = id,
                row['sequence_id'] = id
                row['seqtype'] = seqtype
                row['owner_id'] = ObjectId(self._owner_id)
                row['DateCreated'] = datetime.now()
                row['LastUpdate'] = datetime.now()
                row['Description'] = ""


            print(list_contig_stats)
        
            try: 
                self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
                self._mongo_db_collection.insert_many(list_contig_stats)
                return "parse_denovo_tab: " + filePath + " success"
            except Exception as e:
                print("An exception occurred ::", e)
                return "parse_denovo_tab: " + filePath + " failed"
    
    def update2collection_virulome_tab(self, filePath):
        with open(filePath) as file:
            reader = csv.reader(file, delimiter="\t")
            #ignore reference
            header = next(reader)
           
            for myrow in reader:
                row = []
                for item in myrow:
                    if ";" in item:
                        row.extend(item.split(";"))
                    else:
                        row.append(item)
            
                mydict = dict(zip(header, row))
            
                id = mydict.pop('#FILE').split("/")[0]
                num_found = mydict.pop('NUM_FOUND')

                virulome_list = []
                
                for key, value in mydict.items():
                    if value == '.':
                        value = -1
                    virulome_list.append({'gene': key, 'pctCoverage': value})
                    row['DateCreated'] = datetime.now()
                    row['LastUpdate'] = datetime.now()
                try:
                    self._mongo_db_collection.update_one({"id": id}, 
                        {"$set": {"virulome_num_found": num_found, 
                            "virulome": virulome_list, 
                            "Description": "", 
                            "DateCreated": datetime.now(), 
                            "LastUpdate": datetime.now()}})
                    print("updated virulome collection True")
                except Exception as e:
                    print("An exception occurred ::", e)
                    return "parse_seqstats " + filePath + " failed"

        return "success"

    def update2collection_resistome_tab(self, filePath):
        with open(filePath) as file:
            reader = csv.reader(file, delimiter="\t")
            #ignore reference
            header = next(reader)
           
            for myrow in reader:
                row = []
                for item in myrow:
                    if ";" in item:
                        row.extend(item.split(";"))
                    else:
                        row.append(item)
            
                mydict = dict(zip(header, row))
            
                id = mydict.pop('#FILE').split("/")[0]
                num_found = mydict.pop('NUM_FOUND')

                resistome_list = []
                
                for key, value in mydict.items():
                    if value == '.':
                        value = -1
                    resistome_list.append({'gene': key, 'pctCoverage': value})
                try:
                    self._mongo_db_collection.update_one({"id": id}, {"$set": {"resistome_num_found": num_found, "resistome": resistome_list}})
                    print("updated virulome collection True")
                except Exception as e:
                    print("An exception occurred ::", e)
                    return "parse_seqstats " + filePath + " failed"

        return "success"


    def update2collection_mlst_tab(self, filePath):
        
        with open(filePath) as file:
            reader = csv.reader(file, delimiter="\t")
            #ignore reference
            next(reader)
            mlst_list = []
            for row in reader:
                file = row.pop(0)
                id = file.split("/")[0]
                scheme = row.pop(0)
                st = row.pop(0)
                if st == '-':
                    st = -1
                
                for item in row:
                    index_1 = item.index('(')
                    index_2 = item.index(')') 
                    allele = item[0:index_1]
                    num = item[index_1+1:index_2]
                    mlst_list.append({'allele': allele, 'num': num})
                try:
                    self._mongo_db_collection.update_one({"id": id}, {"$set": {"mlst_scheme": scheme, "mlst_st": st, "mlst_alleles": mlst_list}})
                    print (id + " updated sequence collection True")
                except Exception as e:
                    print("An exception occurred ::", e)
                    return "parse_mlst_tab " + filePath + " failed"

        return "mlst success"

    def add2collection_virulome_tab(self, filePath, seqtype):
            with open(filePath) as file:
                reader = csv.reader(file, delimiter="\t")
                #ignore reference
                header = next(reader)
                results = []
                for myrow in reader:
                    row = []
                    for item in myrow:
                        if ";" in item:
                            row.extend(item.split(";"))
                        else:
                            row.append(item)
                
                    mydict = dict(zip(header, row))
                
                    id = mydict.pop('#FILE').split("/")[0]
                    num_found = int(mydict.pop('NUM_FOUND'))
                    virulome_list = []
                    
                    for key, value in mydict.items():
                        if value == '.':
                            value = -1
                        virulome_list.append({'geneName': key, 'pctCoverage': float(value)})
                    results.append({
                        "id": id,
                        'assembly_id': id,
                        #"sequence_id": id,
                        "seqtype": seqtype,
                        "num_found": num_found, 
                        "profile": virulome_list, 
                        "Description": "", 
                        "DateCreated": datetime.now(), 
                        "LastUpdate": datetime.now(),
                        "owner_id": ObjectId(self._owner_id)
                        
                        })
                try: 
                    self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
                    self._mongo_db_collection.insert_many(results)
                    return "parse_denovo_tab: " + filePath + " success"
                except Exception as e:
                    print("An exception occurred ::", e)
                    return "parse_denovo_tab: " + filePath + " failed"   
            return "success"

    def add2collection_resistome_tab(self, filePath, seqtype):
            with open(filePath) as file:
                reader = csv.reader(file, delimiter="\t")
                #ignore reference
                header = next(reader)
                results = []
                for myrow in reader:
                    row = []
                    for item in myrow:
                        if ";" in item:
                            row.extend(item.split(";"))
                        else:
                            row.append(item)
                
                    mydict = dict(zip(header, row))
                
                    id = mydict.pop('#FILE').split("/")[0]
                    num_found = mydict.pop('NUM_FOUND')
                    resistome_list = []
                    
                    for key, value in mydict.items():
                        if value == '.':
                            value = -1
                        resistome_list.append({'geneName': key, 'pctCoverage': float(value)})
                        
                    results.append({
                        "id": id,
                        'assembly_id': id,
                        #"sequence_id": id,
                        "seqtype": seqtype,
                        "num_found": int(num_found), 
                        "profile": resistome_list, 
                        "Description": "", 
                        "DateCreated": datetime.now(), 
                        "LastUpdate": datetime.now(), 
                        "owner_id": ObjectId(self._owner_id)
                        })
                try: 
                    self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
                    self._mongo_db_collection.insert_many(results)
                    return "parse_denovo_tab: " + filePath + " success"
                except Exception as e:
                    print("An exception occurred ::", e)
                    return "parse_denovo_tab: " + filePath + " failed"   

            return "success"

    def add2collection_mlst_tab(self, filePath, seqtype):
    
        with open(filePath) as file:
            reader = csv.reader(file, delimiter="\t")
            #ignore reference
            next(reader)
            
            results = []
            for row in reader:
                mlst_list = []
                file = row.pop(0)
                id = file.split("/")[0]
                scheme = row.pop(0)
                st = row.pop(0)
                if st == '-':
                    st = -1
                
                for item in row:
                    index_1 = item.index('(')
                    index_2 = item.index(')') 
                    locus = item[0:index_1]
                    allele = item[index_1+1:index_2]
                    mlst_list.append({'locus': locus, 'allele': locus + '_' + allele})
                    
                results.append({
                    "id": id,
                    'assembly_id': id,
                    #'sequence_id': id,
                    "seqtype": seqtype, 
                    "scheme": scheme, 
                    "st": int(st), 
                    "profile": mlst_list, 
                    "Description": "", 
                    "DateCreated": datetime.now(), 
                    "LastUpdate": datetime.now(),
                    "owner_id": ObjectId(self._owner_id)
                    })
                   
            try: 
                self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
                self._mongo_db_collection.insert_many(results)
                return "parse_denovo_tab: " + filePath + " success"
            except Exception as e:
                print("An exception occurred ::", e)
                return "parse_denovo_tab: " + filePath + " failed"   

        return "success"    
    # gff file name is: samplename.gff, samplename will be id
    def add2collection_parse_gff(self, dir, seqtype):
        results = []
        for filename in os.listdir(dir):
            
            
            if filename.endswith(".gff"): 
                print(filename)
                #fname = ntpath.basename(filename)
                sampleid = os.path.splitext(filename)[0]
                
                with open(os.path.join(dir, filename)) as file:
                    
                    for line in file.readlines():
                        data = {}
                        if line[0] == '#':
                            continue
                        elif line[0] == '##FASTA' or re.findall("^>", line[0]):
                            break
                        segment = re.split('\t', line)
                        #print(len(segment))
                        if(len(segment) == 1):
                            print(segment)

                        #print(segment)
                        print(segment[8])
                        attributesString = re.split(';', segment[8].rstrip())
                        attributes = []
                        id = ""
                        for s in attributesString:
                            e = s.split('=')
                            tv = {}
                            if len(e) >= 2 :
                                tag = e[0]
                                value = urllib.parse.unquote(e[1])
                                if tag == "ID":
                                    id = value
                                elif tag == 'inference':
                                    continue
                                else:
                                    attributes.append({'tag':tag, 'value':value})
                                    
                        if not id:
                            id = sampleid + "_" + segment[2] + "_" + str(int(segment[3])-1) + "_" + segment[4]
                        
                        print("myid=" + id)
                        data['id'] = id
                        
                        data['seqid'] = segment[0]
                        data['source'] =segment[1]
                        data['ftype'] =segment[2]
                        data['start'] =int(segment[3])-1
                        data['end'] =int(segment[4])
                        data['score'] =segment[5]
                        data['strand'] =segment[6]
                        data['phase'] =segment[7]
                        data['attr'] = attributes
                         
                        #data['sequence_id'] = sampleid
                        data['assembly_id'] = sampleid
                        data['seqtype'] = seqtype
                        data['Description'] = ""
                        data['owner_id'] = ObjectId(self._owner_id)
                        data['DateCreated'] = datetime.now()
                        data['LastUpdate'] = datetime.now()
                        
                        try:
                            self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
                            self._mongo_db_collection.insert_one(data)
                        except Exception as e:
                            print("load gff An exception occurred ::", e)
                            return "loading gff False"
    

            
def main():
    #add entries to genome collection
    genome = GbaseDataset("ebsdb", "gbase_assembly", "60d4dfba7109403cf2d20636")
    genome.add2collection_denovo_tab("data/gbase/denovo.tab", "TB")

    virulome = GbaseDataset("ebsdb", "gbase_virulome", "60d4dfba7109403cf2d20636")
    virulome.add2collection_virulome_tab("data/gbase/virulome.tab", "TB")

    resistome = GbaseDataset("ebsdb", "gbase_resistome", "60d4dfba7109403cf2d20636")
    resistome.add2collection_resistome_tab("data/gbase/resistome.tab", "TB")

    mlst = GbaseDataset("ebsdb", "gbase_mlst", "60d4dfba7109403cf2d20636")
    mlst.add2collection_mlst_tab("data/gbase/mlst.tab", "TB")



    annotation = GbaseDataset("ebsdb", "gbase_annotation", "60d4dfba7109403cf2d20636")
    annotation.add2collection_parse_gff("data/gbase/gff", "TB")

if __name__ == '__main__':
  main()


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

class IsolateDataset(Dataset):
    
   
        
    def add2collection_assembly_tab(self, filePath, seqtype):
        """
        add new entries into the genome collection
        """
        with open(filePath) as file:
            reader = csv.DictReader(file, delimiter="\t")
            list_contig_stats = list(reader)
            #ERR036228/contigs.fa    177     4254254 4252920 1334    0       213     24035       180126  80234
            #filename        total_length    number  mean_length     longest shortest        N_count Gaps    N50     N50n    N70     N70n    N90     N90n
            #SRR12072643_contigs.fasta       4985234 245     20347.89        155600  514     0       0       38091   41      24130   74      10363   134
            for rowindex, row in enumerate(list_contig_stats):
                id = row['filename'].split("_")[0]
                del row['filename']
                row['count'] = row.pop('number')
                
                row['bp'] = row.pop('total_length')
                row['Ns'] = row.pop('N_count')
                row['gaps'] = row.pop('Gaps')
                row['min'] = row.pop('shortest')
                row['max'] = row.pop('longest')
                row['avg'] = row.pop('mean_length')
                row['N50'] = row.pop('N50')
                #N50n    N70     N70n    N90     N90n
                del row['N50n']
                del row['N70']
                del row['N70n']
                del row['N90']
                del row['N90n']
                for x in row:
                    #if x == 'avg':
                        
                    row[x] = int(float(row[x]))
                
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
                return "add2collection_assembly_tab: " + filePath + " success"
            except Exception as e:
                print("An exception occurred ::", e)
                return "add2collection_assembly_tab: " + filePath + " failed"
    
    def add2isolate_stats(self, filePath, seqtype):
        """
        add new entries into the genome collection
        
        Sample_id       CDS     CRISPR  ncRNA   oriC    rRNA    region  regulatory_region       tRNA    tmRNA
        ERR1679637      4160    3       19      2       3       449     13      46      1
        """
        with open(filePath) as file:
            reader = csv.DictReader(file, delimiter="\t")
            list_stats = list(reader)
            for rowindex, row in enumerate(list_stats):
                id = row['Sample_id']
                del row['Sample_id']
                print(row)
                for x in row:
                    if row[x]:
                        row[x] = int(float(row[x]))
                    else:
                        row[x] = 0
                
                row['id'] = id
                row['assembly_id'] = id
                row['seqtype'] = seqtype
                row['owner_id'] = ObjectId(self._owner_id)
                row['DateCreated'] = datetime.now()
                row['LastUpdate'] = datetime.now()
                row['Description'] = ""


            print(list_stats)
        
            try: 
                self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
                self._mongo_db_collection.insert_many(list_stats)
                return "add2isolate_stats: " + filePath + " success"
            except Exception as e:
                print("An exception occurred ::", e)
                return "add2isolate_stats: " + filePath + " failed"
                   
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
            
                id = mydict.pop('#FILE').split("_")[0]
                num_found = mydict.pop('NUM_FOUND')

                virulome_list = []
                
                for key, value in mydict.items():
                    if value == '.':
                        #value = -1
                        continue
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
                        #value = -1
                        continue
                    resistome_list.append({'gene': key, 'pctCoverage': value})
                try:
                    self._mongo_db_collection.update_one({"id": id}, {"$set": {"resistome_num_found": num_found, "resistome": resistome_list}})
                    print("updated virulome collection True")
                except Exception as e:
                    print("An exception occurred ::", e)
                    return "parse_seqstats " + filePath + " failed"

        return "success"


    

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
                
                    id = mydict.pop('#FILE').split("_")[0]
                    num_found = int(mydict.pop('NUM_FOUND'))
                    virulome_list = []
                    
                    for key, value in mydict.items():
                        if value == '.':
                            #value = -1
                            continue
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
        
    
        
    def parse_amrfinderplus(self, filePath, seqtype):
        
        #column id of the selected metadata downloaded using esearch
        selected_fields = (
            "Name",
            "Gene symbol",
            "Sequence name",
            "Scope",
            "Element type",
            "Class",
            "Method",
            "% Coverage of reference sequence",
            "% Identity to reference sequence"
        )
        
        pp = pprint.PrettyPrinter(indent=4)
        
        
        with open(filePath) as file:
            reader = csv.DictReader(file, delimiter="\t")
            lines = list(reader)
            preid = ""
            id = ""
            results = []
            my_amrs = []
            for rowindex, row in enumerate(lines):
               
                for key, value in row.copy().items():
                    if (key not in selected_fields):
                        del row[key]
                
                
                id = row.pop('Name')
                row['geneName'] = row.pop('Gene symbol')
                row['sequenceName'] = row.pop('Sequence name')
                row['scope'] = row.pop('Scope')
                row['elementType'] = row.pop('Element type')
                row['dclass'] = row.pop('Class')
                row['method'] = row.pop('Method')
                row['pctCoverage'] = row.pop('% Coverage of reference sequence')
                row['pctIdentity'] = row.pop('% Identity to reference sequence')
                
                if preid and id != preid:
                    #change to another samples
                    results.append({
                        "id": preid,
                        'assembly_id': preid,
                        "seqtype": seqtype,
                        "num_found": len(my_amrs), 
                        "profile": my_amrs, 
                        "Description": "", 
                        "DateCreated": datetime.now(), 
                        "LastUpdate": datetime.now(), 
                        "owner_id": ObjectId(self._owner_id)
                        })
                    my_amrs = []
                
                my_amrs.append(row)
                preid = id
                
            results.append({
                        "id": id,
                        'assembly_id': id,
                        "seqtype": seqtype,
                        "num_found": len(my_amrs), 
                        "profile": my_amrs, 
                        "Description": "", 
                        "DateCreated": datetime.now(), 
                        "LastUpdate": datetime.now(), 
                        "owner_id": ObjectId(self._owner_id)
                        })
           
            #print(results)
        
            try: 
                self._mongo_db_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
                self._mongo_db_collection.insert_many(results)
                return "loading json True"
            except Exception as e:
                print("An exception occurred ::", e)
                return "parse_runinfo: " + filePath + " failed"
            return results
    
    
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
                            #value = -1
                            continue
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
    
    def add2mlst_tab(self, filePath, seqtype):
    
        with open(filePath) as file:
            reader = csv.reader(file, delimiter="\t")
            #ignore reference
            #next(reader)
            
            results = []
            for row in reader:
                mlst_list = []
                #file = row.pop(0)
                #id = file.split("/")[0]
                id = row.pop(0)
                scheme = row.pop(0)
                st = row.pop(0)
                # if st == '-':
                #     st = -1
                
                for item in row: 
                    if '(' in item:
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
                    "st": st, 
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
    # genome = IsolateDataset("ebsdb", "isolate_assembly", "60d4dfba7109403cf2d20636")
    # genome.add2collection_denovo_tab("data/isolate/denovo.tab", "TB")

    # virulome = IsolateDataset("ebsdb", "isolate_virulome", "60d4dfba7109403cf2d20636")
    # virulome.add2collection_virulome_tab("data/isolate/virulome.tab", "TB")

    # resistome = IsolateDataset("ebsdb", "isolate_resistome", "60d4dfba7109403cf2d20636")
    # resistome.add2collection_resistome_tab("data/isolate/resistome.tab", "TB")

    # mlst = IsolateDataset("ebsdb", "isolate_mlst", "60d4dfba7109403cf2d20636")
    # mlst.add2collection_mlst_tab("data/isolate/mlst.tab", "TB")
    # annotation = IsolateDataset("ebsdb", "isolate_annotation", "60d4dfba7109403cf2d20636")
    # annotation.add2collection_parse_gff("data/isolate/gff", "TB")
    
    
    genome = IsolateDataset("ebsdb", "isolate_assembly", "60d4dfba7109403cf2d20636")
    genome.add2collection_assembly_tab("data/tb/Report/assembly_stats.tsv", "TB")
    genome.add2collection_assembly_tab("data/cpo/PRJNA640134/Report/assembly_stats.tsv", "CPO")
    genome.add2collection_assembly_tab("data/cpo/PRJNA725227/Report/assembly_stats.tsv", "CPO")
    
    mlst = IsolateDataset("ebsdb", "isolate_mlst", "60d4dfba7109403cf2d20636")
    mlst.add2mlst_tab("data/tb/Report/mlst.tsv", "TB")
    mlst.add2mlst_tab("data/cpo/PRJNA725227/Report/mlst.tsv", "CPO")
    mlst.add2mlst_tab("data/cpo/PRJNA640134/Report/mlst.tsv", "CPO")
    
    resistome = IsolateDataset("ebsdb", "isolate_resistome", "60d4dfba7109403cf2d20636")
    resistome.parse_amrfinderplus("data/tb/Report/amrfinderplus.tsv", "TB")
    resistome.parse_amrfinderplus("data/cpo/PRJNA640134/Report/amrfinderplus.tsv", "CPO")
    resistome.parse_amrfinderplus("data/cpo/PRJNA725227/Report/amrfinderplus.tsv", "CPO")
    
    virulome = IsolateDataset("ebsdb", "isolate_virulome", "60d4dfba7109403cf2d20636")
    virulome.add2collection_virulome_tab("data/tb/Report/vf.tsv", "TB")
    virulome.add2collection_virulome_tab("data/cpo/PRJNA640134/Report/vf.tsv", "CPO")
    virulome.add2collection_virulome_tab("data/cpo/PRJNA725227/Report/vf.tsv", "CPO")
    
    stats = IsolateDataset("ebsdb", "isolate_stats", "60d4dfba7109403cf2d20636")
    stats.add2isolate_stats("data/tb/Report/bakta.tsv", "TB")
    stats.add2isolate_stats("data/cpo/PRJNA640134/Report/bakta.tsv", "CPO")
    stats.add2isolate_stats("data/cpo/PRJNA725227/Report/bakta.tsv", "CPO")
    
    

if __name__ == '__main__':
  main()


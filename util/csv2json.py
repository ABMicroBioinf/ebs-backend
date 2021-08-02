import csv
import json
import pprint
import re
import urllib.parse
#filePath = parse_assembly_stats
def parse_assembly_stats(filePath):

    with open(filePath) as file:
        reader = csv.DictReader(file, delimiter="\t")
        data = list(reader)
        mydict = data[0]
        del mydict["Name"]
        del mydict["ok"]
        mydict["count"] = mydict["no"]
        del mydict["no"]
    return mydict

def parse_virulome(filePath):
    jsonStr = ""
    pp = pprint.PrettyPrinter(indent=4)
    with open(filePath) as file:
        reader = csv.DictReader(file, delimiter="\t")
        mylist = list(reader)
        for data in mylist:
            del data['#FILE']
            data['PCT_COVERAGE'] = data['%COVERAGE']
            del data['%COVERAGE']
            data['PCT_identity'] = data['%IDENTITY']
            del data['%IDENTITY']
        
    return mylist

def parse_amr(filePath):
    jsonStr = ""
    pp = pprint.PrettyPrinter(indent=4)
    with open(filePath) as file:
        reader = csv.DictReader(file, delimiter="\t")
        mylist = list(reader)
        for data in mylist:
            del data['#FILE']
            data['PCT_COVERAGE'] = data['%COVERAGE']
            del data['%COVERAGE']
            data['PCT_identity'] = data['%IDENTITY']
            del data['%IDENTITY']
         
    return mylist

def parse_gff(filePath):
    
    records = []
    cat = {}
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
            
            for s in attributesString:
                e = s.split('=')
                tv = {}
                if len(e) >= 2 :
                    tv["tag"] = e[0]
                    tv["value"] = urllib.parse.unquote(e[1])
                    attributes.append(tv)
            

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
            
    return records

def main():
    result = []
    data = {}
    output = parse_assembly_stats("SRR1162491/contigs.summary.tab")
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(output)
    # print(type(output))
    data["contig_stats"] = output
    virulome_list = parse_virulome("SRR1162491/virulome.tab")
    #print(virulome_list)
    data["virulome"] = virulome_list
    data["amr"] = parse_amr("SRR1162491/resistome.tab")
    data["gff"] = parse_gff("SRR1162491/contigs.gff")

    result.append(data)
    #result.append(virulome_list)
    print(json.dumps(result))
    pass


if __name__ == '__main__':
  main()


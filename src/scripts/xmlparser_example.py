#Python code to illustrate parsing of XML files
# importing the required modules
import lxml.etree 

def parseXML(xmlfile):
  
    tree = lxml.etree.parse(xmlfile)
    root = tree.getroot()
    for elem in tree.iter():
        #print(type(elem))
        print(elem.tag)
        print(elem.text)
        print("parent=")
        print(elem.getparent())
          


    newsitems = []
    return newsitems
      
def main():
    
    # parse xml file
    newsitems = parseXML('data/seq/projects.xml')
  
if __name__ == "__main__":
  
    # calling main function
    main()
import pandas as pd
import re
rawdata=pd.read_csv("pubandengr.csv")
rawdata.fillna("UNK")
#rawdata.strip("[]()|")
for x in rawdata.index:
    if re.search("Engelmann Plate", rawdata.loc[x, "ENGRAVER"]):
        rawdata.loc[x,"ENGRAVER"]="Engelmann"
    if re.search("V. Grosse", rawdata.loc[x, "ENGRAVER"]):
        rawdata.loc[x,"ENGRAVER"]="V. Grosse"
    if re.search("Breitkopf", rawdata.loc[x, "ENGRAVER"]):
        rawdata.loc[x,"ENGRAVER"]="Breitkopf und Hartel"
        




#print(rawdata)
pubs=rawdata['PUBLISHER'].drop_duplicates().tolist()
engs=rawdata['ENGRAVER'].drop_duplicates().tolist()

#print(pubs)
#print(engs)
#print(len(engs))

# Create a dataframe filled with zeroes and label the rows and columns
pubengcum = pd.DataFrame(0, index=pubs, columns=engs)

for x in rawdata.index:
    try:
        y= pubengcum.loc[rawdata.loc[x,"PUBLISHER"],rawdata.loc[x,"ENGRAVER"]]
        pubengcum.loc[rawdata.loc[x,"PUBLISHER"],rawdata.loc[x,"ENGRAVER"]]=y+1
    except IndexError:
        continue

#print(pubengcum)
print(pubengcum.sum().to_string())
import random
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
az="abcdefghijklmnopqrstuvwxyz"
def acakhuruf(char=5,count=1,case="semua"):
    a_z=""
    l=list()
    if case=="semua":
        a_z=AZ+az
    elif case=="besar":
        a_z=AZ
    elif case=="kecil":
        a_z=az
    for y in range(count):
        r=""
        for x in range(char):
            r+=a_z[random.randint(0,len(a_z)-1)]
        l.append(r)
    if count==1:
        return l[0]
    else:
        return l

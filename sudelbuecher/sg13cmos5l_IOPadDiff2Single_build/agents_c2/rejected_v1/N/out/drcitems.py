import sys,glob,re
c=sys.argv[1]
for f in glob.glob("logs/drc_%s/*_full.lyrdb"%c):
    t=open(f).read()
    for m in re.finditer(r"<item>(.*?)</item>",t,re.S):
        b=m.group(1)
        cat=re.search(r"<category>(.*?)</category>",b).group(1)
        vals=re.findall(r"<value>(.*?)</value>",b)
        print(cat,vals[:2])

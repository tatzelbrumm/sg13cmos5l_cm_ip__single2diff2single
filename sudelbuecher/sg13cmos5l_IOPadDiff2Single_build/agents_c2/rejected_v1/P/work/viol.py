import re,glob,sys
d=sys.argv[1]
for f in glob.glob(d+"/*.lyrdb"):
    t=open(f).read()
    descr={m.group(1):m.group(2) for m in re.finditer(r"<category>\s*<name>([^<]*)</name>\s*<description>([^<]*)</description>",t)}
    for m in re.finditer(r"<item>(.*?)</item>",t,re.S):
        it=m.group(1)
        cat=re.search(r"<category>'?([^<']*)'?</category>",it).group(1)
        val=re.findall(r"<value>([^<]*)</value>",it)
        print(cat, descr.get(cat,"")[:70], val[:2])

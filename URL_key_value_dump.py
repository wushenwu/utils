import sys

d_key_value = {}

def dumpInfoCnt(filename, d_key_value):
    fw = open(filename, 'w')
    
    sorted_key_value = sorted(d_key_value.items(), key=lambda item: len(item[1]), reverse=True)
    for item in sorted_key_value:
        key = item[0]
        value = item[1]
        fw.write("%s\t_cnt_\t%d\n"%(key, len(value)))
        for v in value:
            fw.write("\t%s\n"%v)
    fw.close()

def main():
    global d_key_value
    with open(sys.argv[1], 'rb') as fr:
        for line in fr:
            #mobincome.org/sdk_api.php?id=fe63585f-fe4f-447a-b6dc-f8ade96c907e&type=timer
            items = line.strip().partition('?')
            interface = items[0].rpartition('/')[2]
            d_key_value.setdefault('interface', set()).add(interface)
            if not interface:
                print(line)
            
            query = items[2]
            if not query:
                continue
            parts = query.split('&')
            for part in parts:
                if part.find('=') == -1:
                    continue
                
                try:
                    key, value = part.split('=')
                except:
                    continue
                    
                d_key_value.setdefault(key, set()).add(value)
    
    dumpInfoCnt(sys.argv[1] + '_key_value.txt', d_key_value)
        
if __name__ == "__main__":
    main()
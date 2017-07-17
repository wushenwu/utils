import os
import sys
import hashlib

d_name_md5 = {} # {name : [md51, md52]}
   
def HashDeep(parent, apkpath):
    '''
    get hashes for all the files under the curdir, and save them into file
    '''
    global d_name_md5
    
    paths_to_hash = []
    rootparam = os.path.join(parent, apkpath)
        
    for root, subdirs, files in os.walk(rootparam):
        for filename in files:
            path = os.path.join(root, filename)
            name = path[len(rootparam) + 1:]
            paths_to_hash.append([path, name])
    
    if 0 == len(paths_to_hash):
        return
        
    fw = open(os.path.join(parent, apkpath + '_hash.txt'), 'w')
    for ele in paths_to_hash:
        path = ele[0]
        name = ele[1]
        fr = open(path, "rb")
        hash = hashlib.md5(fr.read()).digest()
        hash = hash.encode('hex')
        fr.close()
        #print '{0} : {1}'.format(hash, name)
        fw.write('{0} : {1}'.format(hash, name))
        fw.write('\n')
        
        if name not in d_name_md5.keys():
            d_name_md5[name] = []
            
        if hash not in d_name_md5[name]:
            d_name_md5[name].append(hash)
    
    fw.close()

def Classify(curdir):
    '''
    walk all the apk files under the current directory, and group them by size
    '''
    d_size_apk = {}  # {size : [apk1, apk2]}
    files = os.listdir(curdir)
    for filename in files:
        
        if -1 == filename.find('.apk'):
            pass
            
        st = os.stat(os.path.join(curdir, filename))
        #just give a similar calc
        size = (st.st_size + 9999)/10000  #1KB  1024
        if size not in d_size_apk.keys():
            d_size_apk[size] = []
        d_size_apk[size].append(filename)
    
    global d_name_md5
    for key, value in d_size_apk.iteritems():
        print key, value
        print 
        
        '''
        group by size
        '''
        d_name_md5 = {}
        for apk in value:
            #HashDeep(os.path.join(curdir, apk[ :apk.find('.apk')]))
            HashDeep(curdir, apk[ :apk.find('.apk')])
    
        '''
        check within the group
        '''
        for name, md5s in d_name_md5.iteritems():
            if 1 == len(md5s):
                continue
            
            if name.find(r'res\draw') != -1: #|| name.find('apktool.yml') != -1:
                continue
                
            print '\t',name, md5s
        print
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit(-1)
    
    curdir = sys.argv[1]
    Classify(curdir)
#

root_regex={r'href=(["\'])http://developer.android.com':r'href=\1{0}', r'href=(["\'])/':r'href=\1{0}/'}
regex={'http[s]*://www.google.com/jsapi':'http://ajax.useso.com/jsapi',
        'http://fonts.googleapis.com':'http://fonts.useso.com',
        r'//www.google.com/jsapi':'http://ajax.useso.com/jsapi'}


import os
import os.path
import re
import string
import sys

class DirInf:
    def __init__(self,path,subdirs,files):
        self.path=path
        self.subdirs=subdirs
        self.files=files
        

class Walker:
    def __init__(self, top):
        self.top=os.path.abspath(top)
        self.tabsize=4

    def exec(self):
        for d, subdirs, files in os.walk(self.top):
            self.walk_in_dir(DirInf(d,subdirs,files))
            
    def walk_in_dir(self, dirInf):
        for i in dirInf.files:
            self.tryReplace(dirInf.path, i)

    def tryReplace(self, dirPath, file):
        path = os.path.sep.join([dirPath, file])
        if self.isHtml(path) is True:
            self.replace(path)
            
    def isHtml(self, filePath):
        #print(filePath)
        if len(filePath) < 3:
            return False
        t=filePath.lower()
        #print(t)
        if t.endswith("html") or t.endswith("htm"):
            return True
        return False
    
    def calcRelativePathToTop(self, path):
        
        count = path.count(os.path.sep) - self.top.count(os.path.sep) - 1
        print("log:",path,count)
        rpath=None
        for i in range(0, count):
            if None is not rpath:
                rpath = rpath + "/.."
            else:
                rpath = ".."
        if rpath is None:
            rpath = "."
        return rpath
    def replace_root(self, l, relativeTopPath):
        nl=l
        for i in root_regex:
            rp = root_regex[i].format(relativeTopPath)
            nl = re.sub(i, rp, nl)
        return nl

    def replace(self, path):
        #print("html:"+path)
        tmp=path+'.tmp'
        
        f=open(path, 'rb')
        n=open(tmp,'wb+')
        lineCounter=0;
        relativeTopPath=self.calcRelativePathToTop(path)
        self.logout("file:{0}".format(path));
        if f is not None:
            for i in f:
                lineCounter = lineCounter+1
                l = i.decode('utf-8')
                nl=self.replace_root(l, relativeTopPath)
                                
                # relative to root folder
                if nl != l:
                    self.logout("\t{0}:{1} <- {2}".format(lineCounter, nl, l).expandtabs(self.tabsize))
                    l=nl
                # replace to cdn 
                for k in regex:
                    nl=re.sub(k,regex[k], l)
                    if nl != l:
                        self.logout("\t{0}:{1}".format(lineCounter, nl).expandtabs(self.tabsize))
                        l = nl
                n.write(l.encode('utf-8'))
        n.close()
        f.close()
        origin=path+".origin"
        if  os.path.exists(origin):
            os.remove(origin)
        os.rename(path, origin)
        os.rename(tmp, path)
    def logout(self, s):
        try:
            print(s)
        except Exception as e:
            print(e)
            
        

        
if __name__ == "__main__":
    walker=Walker(sys.argv[1])
    walker.exec()
    

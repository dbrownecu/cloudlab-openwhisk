import cv2
from timeit import default_timer as timer
import os
import json
from os.path import isfile,join
from cloudant.client import CouchDB
import time

K_DBNAME = "frshimg"
K_DB2NAME = "resizeimg"
K_PREFIX = "resized-{}"
K_FILE_TYPE="image/png"

def write2db(fn, dbname, user, passwd, url):
    db_client = CouchDB(user,passwd, url=url, connect=True)
    if not db_client.session()['ok']:
        return ("cannot open database with {}:{},@{}".format(user, passwd, url))
    db_inst = db_client[dbname]
    resized_fn =K_PREFIX.format(fn)
    dta = {
        '_id':"{}".format(int(time.time()*1000)),
        'name':fn
        }
    doc = db_inst.create_document(dta)
    print("doc is {}".format(doc))
    fh = open(join('/tmp',resized_fn),'rb')
    if fh:
        print("Writing {}".format(resized_fn))
        f_dta = bytearray(fh.read())
        ret=doc.put_attachment(fn, K_FILE_TYPE,f_dta)
        print("attachment status: {}".format(ret))
        doc.save()
        fh.close()
    db_client.disconnect()




def get_fn(inp):
    for i in inp:
        return i

def write_file(pth,fn, dta):
    fullpth = join(pth,fn)
    with open(fullpth,'wb') as fh:
        fh.write(dta)

def preprocess_image(d_pth,fn):
    img = cv2.imread(join(d_pth,fn))
    img2 = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    xxx = join(d_pth,K_PREFIX.format(fn))
    cv2.imwrite(xxx,img2)


def test_count(user, passwd, url, num_recs):
    print("user {}, passwd{}, url {}, numrecs {}".format(user, passwd, url, num_recs))
    db_client = CouchDB(user, passwd, url=url, connect=True)
    db_inst = db_client[K_DBNAME]
    rec_count = db_inst.doc_count()
    keys = db_inst.keys(remote=True)
    byte_count = 0
    rec_total = 0
    start = timer()
    ctr = 0
    while ctr < num_recs:
        i = keys[ctr]
        doc = db_inst.get(i, remote=True)
        img_dict = doc['_attachments'].keys()
        img_name = get_fn(img_dict)
        img = doc.get_attachment(img_name)
        write_file('/tmp',img_name,img)
        preprocess_image('/tmp',img_name)
        write2db(img_name,K_DB2NAME, user,passwd,url)
        ctr +=1



if __name__ == '__main__':
    user = os.getenv('FRSH_USR') # = admin
    passwd = os.getenv('FRSH_PWD') # = $(kubectl get secret djb-couch-couchdb -o go-template='{{ .data.adminPassword }}' | base64 --decode)
    url = os.getenv('FRSH_URL')  # = http://ipaddress_of_server:5984
    pth = os.getenv('FRSH_FILE_PATH') # = file path
    test_count(user,passwd,url,9)

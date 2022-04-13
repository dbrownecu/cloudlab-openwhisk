import sys
import os
from timeit import default_timer as timer
import json

from cloudant.client import CouchDB

K_DBNAME = "frshimg"


def get_fn(inp):
    for i in inp:
        return i


def get_records(user, passwd, url):
    db_client = CouchDB(user, passwd, url=url, connect=True);
    db_inst = db_client[K_DBNAME]
    rec_count = db_inst.doc_count()
    # print('The database contains {} records'.format(rec_count))
    keys = db_inst.keys(remote=True)
    # print('we have the following keys {} '.format(keys))
    byte_count = 0
    rec_total = 0
    start = timer()
    for i in keys:
        doc = db_inst.get(i, remote=True)
        img_dict = doc['_attachments'].keys()
        img_name = get_fn(img_dict)
        img = doc.get_attachment(img_name)
        byte_count += len(img)
        rec_total += 1
    end = timer() - start

    status = {"recs_indb": rec_count, "recs_processed":rec_total, "bytes_read": byte_count, "elapsed_time": end}
    return {
        "statusCode": 200,
        "body": json.dumps(({
            "label": status,
        })),
    }


if __name__ == '__main__':
    user = os.getenv('FRSH_USR')  # = admin
    passwd = os.getenv('FRSH_PWD')  # = $(kubectl get secret djb-couch-couchdb -o go-template='{{ .data.adminPassword }}' | base64 --decode)
    url = os.getenv('FRSH_URL')  # = http://ipaddress_of_server:5984

    recval = get_records(user, passwd, url)

    print('got some data {}'.format(recval))


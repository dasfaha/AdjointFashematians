#!/usr/bin/env python

import csv
import os
import sys
from pymongo import MongoClient

client = MongoClient(os.environ.get('MONGODB_URL'))
db = client.social_influencers
persons = db.persons
rankings = db.rankings

def find_one_or_create(doc):
    res = persons.find_one(doc)
    if res:
        return res['_id']
    return persons.save(doc)

def read_file(filename):
    with open(filename) as f:
        r = csv.reader(f)
        header = r.next()
        choice = 1 if 'Choice' in header else 0
        keys_A = [k[2:] for k in header if k.startswith('A')]
        keys_B = [k[2:] for k in header if k.startswith('B')]
        assert keys_A == keys_B
        pivot = choice + len(keys_A)
        for row in r:
            A_id = find_one_or_create(dict(zip(keys_A, row[choice:pivot])))
            B_id = find_one_or_create(dict(zip(keys_B, row[pivot:])))
            rankings.save({'A': A_id, 'B': B_id, 'choice': row[0] if choice else None})

def main():
    if len(sys.argv) == 1:
        print "Usage: %s FILE1 [FILE2 ...]" % sys.argv[0]
        sys.exit(1)
    for arg in sys.argv[1:]:
        read_file(arg)

if __name__ == '__main__':
    sys.exit(main())

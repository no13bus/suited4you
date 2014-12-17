## mongo settings
import pymongo
conn = pymongo.Connection("localhost", 27017)
db = conn["suited4you"]
coll = db.project
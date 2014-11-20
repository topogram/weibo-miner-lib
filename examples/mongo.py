import pymongo

# get data from mongo
host="localhost"
port=27017
connection = Connection(host=host, port=port)
db = connection["topogram"]
meme_id=ObjectId("546cdd54ab4fc838d23cd947")
meme=db["memes"].find_one({ "_id" : meme_id })


# # save to mongo
# test_id=db.test.insert(json.loads(weibo.to_JSON()))
# db.memes.update({
#                '_id':meme_id
#                },{
#                '$set':{
#                 "timeframes": json.loads(weibo.to_JSON())
#                  }
#             })
# print "saved in mongo as ",test_id

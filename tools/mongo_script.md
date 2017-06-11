
db.getCollection('doubanUsers').find().count()

db.getCollection('doubanUsers').find({joined_groups:{$size:0}})


db.getCollection('doubanUsers').aggregate([
    {$unwind:'$joined_groups'},
    {$group:{
       _id:{id:'$user_id',name:'$user_name'},
       groups:{$push:'$joined_groups.group_name'}
     }},
     {$match:{groups:{$all:["上海租房"]}}}
])


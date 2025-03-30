# Python-treehole
- Design for PKU Junior Lesson "Introduction to Database"

# 有关数据库的说明
## hole数据库 (存放树洞原文)
- hole_id (primary key)         
- release_time
- user_id
- content

## comment数据库 (存放树洞评论)
- comment_id (primary key) 
- hole_id (foreign key)
- release_time 
- user_id
- userNO

## comment_relation数据库 (判断ABCD)
- hole_id
- user_id (combined primary key with hole_id)
- userNO

## user数据库 (存放用户信息)
- user_id (primary key)
- username
- password
- create_time
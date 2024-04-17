# from filexdb import FileXdb
# from bcrypt import hashpw, gensalt

# db = FileXdb("data", "./")

# admindata = db.collection("admin")
# themes = db.collection("themes")

# themes.insert({"name": "cubs", themes: []})
# themes.insert({"name": "titans", themes: []})

# # admindata.insert(
# #     {"password": hashpw("admin".encode(), gensalt()).decode(), "username": "admin"}
# # )

# # data = admindata.find(query={"username": "admin"})
# # print(data)


from tinydb import TinyDB, Query
from bcrypt import hashpw, gensalt, checkpw

db = TinyDB("data.json")

db.insert(
    {
        "admindata": {
            "password": hashpw("admin".encode(), gensalt()).decode(),
            "username": "admin",
        }
    }
)

db.insert({"name": "cubs", "data": []})

db.insert({"name": "titans", "data": []})

# q = Query()
# print(db.search(q.admindata.username == "admin")[0]["admindata"])

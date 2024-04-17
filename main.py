from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
from bcrypt import hashpw, gensalt, checkpw
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from tinydb import TinyDB, Query, where

# load api key from env
from dotenv import load_dotenv

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

db = TinyDB("data.json")


client = ElevenLabs(
    api_key=elevenlabs_api_key,
)

voice_id = "jsCqWAovK2LkecY7zXl4"

print("Starting Server: keys loaded")


@app.route("/audio/<audioname>/<content>")
def getAudio(audioname, content):
    print(audioname, content)
    audioname = audioname.replace("%20", " ")
    content = content.replace("%20", " ")
    if os.path.exists(f"./audios/{audioname.lower()}.mp3"):
        return send_file(f"./audios/{audioname.lower()}.mp3", as_attachment=True)

    else:
        if audioname.split("-")[-1] == "definition":
            audio = client.generate(text=content, voice=voice_id)
            save(audio, f"./audios/{audioname.lower()}.mp3")
            return send_file(f"./audios/{audioname.lower()}.mp3", as_attachment=True)

        elif audioname.split("-")[-1] == "usage":
            audio = client.generate(
                text=content.replace("$$sep$$", "\n"), voice=voice_id
            )
            save(audio, f"./audios/{audioname.lower()}.mp3")
            return send_file(f"./audios/{audioname.lower()}.mp3", as_attachment=True)
        else:
            audio = client.generate(text=audioname, voice=voice_id)
            save(audio, f"./audios/{audioname.lower()}.mp3")
            return send_file(f"./audios/{audioname.lower()}.mp3", as_attachment=True)


@app.route("/images/<imagename>")
def getImage(imagename):
    imagename = imagename.replace("%20", " ")
    return send_file(f"./images/{imagename}.png", as_attachment=True)


@app.route("/authenticate", methods=["POST"])
def checkPassword():
    data = request.json
    password = data["password"]

    q = Query()
    admin = db.search(q.admindata.username == "admin")[0]["admindata"]

    if checkpw(password.encode(), admin["password"].encode()):
        return jsonify({"authenticated": True}), 200
    else:
        return jsonify({"authenticated": False}), 200


@app.route("/themes", methods=["POST"])
def getThemes():
    q = Query()
    data = db.search(where("name").matches("cubs|titans"))

    return jsonify(data), 200


@app.route("/getData", methods=["POST"])
def getData():
    q = Query()
    req = request.json
    name = req["name"]
    grade = req["grade"]
    theme = req["theme"]
    data = db.search(where("name") == name)

    # get words where data.data.number = grade and data.data.themes[x].name = theme
    for i in data[0]["data"]:
        if i["number"] == grade:
            for j in i["themes"]:
                if j["name"] == theme:
                    return jsonify(j["words"]), 200

    return jsonify([]), 200


@app.route("/save", methods=["POST"])
def saveData():
    rawdata = eval(request.form["data"])
    data = rawdata["data"]
    name = rawdata["name"]

    print(name, data)
    # print(request.files, eval(request.form["data"]))

    for i in request.files:
        # save image by name in images folder
        request.files[i].save(f"./images/{i}.png")

    db.update({"data": data}, where("name") == name)
    #
    return jsonify({"saved": True}), 200


if __name__ == "__main__":
    app.run(debug=True)

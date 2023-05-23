from flask import Flask, request, jsonify
from pathlib import Path

import json

from classes.music import Music

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

def update_data(music_data:dict):
    with open(f'{BASE_DIR}/data/catalog.json', 'w') as file:
        file.write(json.dumps(music_data, indent=4))

def load_data():
    with open(f'{BASE_DIR}/data/catalog.json') as file:
        return json.load(file)    

def all_musics():
    data = load_data()
    return data.get('musicCatalog', [{}])

def search_music(id, index=False):
    data = load_data()
    list_music = data.get('musicCatalog', [{}])
    if index:
        found_index = [index_ for index_ in range(len(list_music)) if list_music[index_].get("id", "") == int(id)]
        if len(found_index) > 0:
            return found_index[-1]
        else:
            return -1
    found_music = [music for music in list_music if music.get("id", "") == int(id)]
    if len(found_music) > 0:
        return found_music[-1]
    else:
        return False

def validate_music(music:dict):
    type_validation = {
        "id": lambda data : type(data) == int,
        "name": lambda data: type(data) == str,
        "artist" : lambda data: type(data) == str,
        "album": lambda data: type(data) == str,
        "views": lambda data: type(data) == int
    }
    data_validation = []
    try:
        for key, value in music.items():
            data_validation.append(type_validation.get(key, False)(value))
        print("data validation: ", data_validation)
        if False in data_validation:
            return False
        else:
            request_music = Music(
                music.get("id", None),
                music.get("name", ""),
                music.get("artist", ""),
                music.get("album", ""),
                music.get("views", None)
            )
            return request_music
    except:
        return {}

@app.route("/", methods=['GET'])
def main_page():
    return jsonify(
        {"app": "online", "base dir": f"{BASE_DIR}"}
        ), 200

@app.route("/music", methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.get("/music/<id>")
@app.delete("/music/<id>")
def set_music(id:str=None):
    if request.method == 'GET':
        if id:
            music = search_music(id, True)
            if (music >= 0):
                data = load_data()
                obj = data.get("musicCatalog", [{}])[music]
                obj['views'] += 1
                data[music] = obj
                update_data(data)
                return jsonify(obj), 200
            else:
                return jsonify(
                    {"error": f"Id {id} not found"}
                ), 404
        else:
            return jsonify({"musicCatalog": all_musics()}), 200
        
    elif request.method == 'POST':
        music_obj = validate_music(request.json)
        if type(music_obj) == Music:
            data = load_data()
            data.get("musicCatalog", [{}]).append(vars(music_obj))
            update_data(data)
            return jsonify(
                {"Insert": "Success Operation"}
            ), 201
        else:
            return jsonify(
                {"Insert": "Failed Operation"}
            ), 400

    elif request.method == 'PUT':
        music_obj = validate_music(request.json)
        if type(music_obj) == Music:
            index = search_music(music_obj.id, True)
            if index >= 0:
                #update
                data = load_data()
                data.get("musicCatalog", [{}])[index]['name'] = music_obj.name
                data.get("musicCatalog", [{}])[index]['artist'] = music_obj.artist
                data.get("musicCatalog", [{}])[index]['album'] = music_obj.album
                data.get("musicCatalog", [{}])[index]['views'] = music_obj.views
                update_data(data)
                return jsonify(
                    {"Update": "Success Operation"}
                )
            else:
                return jsonify(
                    {"Update": f"Id {music_obj.id} not found"}
                ), 404
        else:
            return jsonify(
                {"Update": "Failed Operation"}
            ), 400
        
    elif request.method == 'DELETE':
        if id:
            print(id)
            index = search_music(id, True)
            if index >= 0:
                print(index)
                data = load_data()
                data.get("musicCatalog", [{}]).pop(index)
                update_data(data)
                return jsonify(
                    {"Delete":"Success Operation"}
                ), 200
            else:
                return jsonify(
                    {"Delete":f"Id {id} not found"}
                ), 400
        else:
            return jsonify(
                {"Delete":"Id not found"}
            ), 400
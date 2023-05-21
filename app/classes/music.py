class Music:
    def __init__(self, id:int, name:str, artist:str, album:str, views:int):
        self.id = id
        self.name = name
        self.artist = artist
        self.album = album
        self.views = views

    def __str__(self):
        return f"Id: {self.id}, Nome: {self.name}, artista: {self.artist}, album: {self.album}, visualizacoes: {self.views}"

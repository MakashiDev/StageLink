"""
This agent is responsible for managing the show list.
"""


import json


class ShowAgent:

    def __init__(self):
        """
        This method is responsible for initializing the show agent.
        """
        shows = []
        showsPath = "json/showList.json"

        self.shows = shows
        self.showsPath = showsPath
        self.get_show_list()

    def get_show_list(self):
        jsonFile = open(self.showsPath, "r")
        self.shows = json.load(jsonFile)["shows"]
        print(self.shows)
        jsonFile.close()

    def save_show_list(self):
        jsonFile = open(self.showsPath, "w")
        json.dump(self.shows, jsonFile)
        jsonFile.close()

    def select_show(self, show_id):
        """
        This method is responsible for selecting a show by ID.
        """
        if show_id is None:
            return None

        print("Show ID: " + str(show_id))

        for show in self.shows:
            if show["id"] == int(show_id):
                print("Show selected: ")
                print(show)
                print("--------------------")
                return show

    def create_show(self, name, type, actCount):
        id = len(self.shows) + 1
        show = {
            "name": name,
            "type": type,
            "actCount": actCount,
            "id": id,
            "cueCount": 0,
        }

        self.shows.append(show)
        self.save_show_list()

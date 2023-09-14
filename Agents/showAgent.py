"""
This agent is responsible for managing the show list.
"""


import json
from Agents.cueAgent import CueAgent


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
        self.cues = CueAgent()

        self.currentShow = None
        self.currentAct = None
        self.currentScene = None

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

    def start_show(self, show_id):
        if show_id is None:
            return None

        show = self.select_show(show_id)
        if show is None:
            return None

        self.cues.set_show_id(show_id)
        self.cues.get_list()
        self.cues.start()

        self.currentShow = show_id
        self.currentAct = 1
        self.currentScene = 1

        return self.currentInfo()

    def currentInfo(self):
        show = self.select_show(self.currentShow)
        if show is None:
            return None

        return {
            "name": show["name"],
            "type": show["type"],
            "actCount": show["actCount"],
            "act": self.currentAct,
            "scene": self.currentScene,
            "id": show["id"],
            "cueCount": show["cueCount"],
            "currentCue": self.cues.currentCue,
        }

    def next_cue(self):
        self.cues.next()

    def previous_cue(self):
        self.cues.previous()

    def get_current_cue(self):
        return self.cues.get_current()

    def next_scene(self):
        self.currentScene += 1
        return self.currentScene

    def previous_scene(self):
        self.currentScene -= 1
        return self.currentScene

    def next_act(self):
        self.currentAct += 1
        return self.currentAct

    def previous_act(self):
        self.currentAct -= 1
        return self.currentAct

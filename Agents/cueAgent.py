import json


class CueAgent:
    def __init__(self):
        show_id = None
        cueList = []

        self.show_id = None
        self.cueList = cueList

        self.currentCue = None

    def set_show_id(self, show_id):
        """ 
        This method is responsible for setting the show ID.
        """
        self.show_id = show_id
        self.get_list()

    def get_show(self):
        """
        This method is responsible for selecting a show by ID.
        """
        if self.show_id is None:
            return None

        print("Show ID: " + str(self.show_id))

        shows = []
        showsPath = "json/showList.json"
        jsonFile = open(showsPath, "r")
        shows = json.load(jsonFile)["shows"]
        jsonFile.close()

        for show in shows:
            if show["id"] == int(self.show_id):
                print("Show selected: ")
                print(show)
                print("--------------------")
                return show

    def get_list(self):
        if self.show_id is None:
            # throw err
            raise Exception("No show selected")

        show = self.get_show()
        if show is None:
            return None
        self.cueList = show["cues"]

    def save_list(self):
        if self.show_id is None:
            # throw err
            raise Exception("No show selected")
        jsonList = open(self.jsonPath, "w")
        json.dump(self.cueList, jsonList)
        jsonList.close()

    def get(self, cue_id):
        if self.show_id is None:
            # throw err
            raise Exception("No show selected")
        if cue_id is None:
            return None
        for cue in self.cueList:
            if cue["id"] == cue_id:
                return cue

    def create(self, name):
        if self.show_id is None:
            # throw err
            raise Exception("No show selected")
        id = len(self.cueList) + 1
        cue = {
            "name": name,
            "id": id,
        }

        self.cueList.append(cue)
        self.save_cue_list()

    def start(self):
        show = self.get_show()
        if show is None:
            return None
        self.currentCue = show["cues"][0]
        return self.currentCue

    def nextCue(self):
        if self.currentCue is None:
            return None
        for cue in self.cueList:
            if cue["id"] == self.currentCue["id"] + 1:
                self.currentCue = cue
                return cue
        return None

    def previousCue(self):
        if self.currentCue is None:
            return None
        for cue in self.cueList:
            if cue["id"] == self.currentCue["id"] - 1:
                self.currentCue = cue
                return cue
        return None

    def selectCue(self, cue_id):
        if cue_id is None:
            return None
        for cue in self.cueList:
            if cue["id"] == cue_id:
                self.currentCue = cue
                return cue
        return None

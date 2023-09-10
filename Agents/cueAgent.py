import json
from Agents.showAgent import ShowAgent


class CueAgent:
    def __init__(self, show_id):
        show_id = None
        cueList = []

        self.show_id = show_id
        self.cueList = cueList

    def get_cue_list(self):
        show = ShowAgent.select_show(self.show_id)
        if show is None:
            return None
        self.cueList = show["cues"]

    def save_cue_list(self):
        jsonList = open(self.jsonPath, "w")
        json.dump(self.cues, jsonList)
        jsonList.close()

    def get_cue(self, cue_id):
        if cue_id is None:
            return None
        for cue in self.cues:
            if cue["id"] == cue_id:
                return cue

    def create_cue(self, name):
        id = len(self.cues) + 1
        cue = {
            "name": name,
            "id": id,
        }

        self.cues.append(cue)
        self.save_cue_list()

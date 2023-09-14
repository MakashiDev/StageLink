"""
This agent is responsible for managing the show list.
"""


import json
import os
import time


class ShowAgent:
    """ 
    This agent is responsible for managing the show list.
     """

    def __init__(self):
        """
        This agent is responsible for managing the show list.
        """
        self.shows = []
        self.showsFolder = "../shows"
        self.show = None
        self.showPath = None

        self.act = None

        self.load()

    def load(self):
        """
        Loads the shows from the shows folder.
        """
        for show in os.listdir(self.showsFolder):
            if show.endswith(".json"):
                with open(os.path.join(self.showsFolder, show)) as f:
                    showFile = json.load(f)
                    name = showFile.get("name")
                    slug = showFile.get("slug")
                    self.shows.append({"name": name, "slug": slug})
        return self.shows

    def select(self, slug):
        """
        Selects a show from the list of shows.
        """
        for show in self.shows:
            if show.get("slug") == slug:
                self.show = json.load(
                    open(os.path.join(self.showsFolder, slug + ".json")))
                self.showPath = os.path.join(self.showsFolder, slug + ".json")
                self.act = Acts(self.show)

                return show

    def get(self):
        """
        Returns the currently selected show.
        """
        return self.show


class Acts:

    def __init__(self, show):
        """ 
        This agent is responsible for managing the acts.
        """
        self.show = show
        self.actIndex = None
        self.currentAct = None
        self.act = None
        self.actCount = None

        self.scene = None

        self.load()

    def load(self):
        """
        Loads the acts from the show.
        """
        self.act = self.show.get("acts")
        self.actCount = len(self.act)
        self.actIndex = 1
        self.currentAct = self.act[self.actIndex - 1]

        self.scene = Scenes(self.get())

        return self.act

    def previous(self):
        """
        Returns the previous act.
        """
        if self.actIndex > 1:
            self.actIndex -= 1
        else:
            self.actIndex = self.actCount
        return self.actIndex

    def next(self):
        """
        Returns the next act.
        """
        if self.actIndex < self.actCount:
            self.actIndex += 1
        else:
            self.actIndex = 1
        return self.actIndex

    def get(self):
        """
        Returns the current act.
        """
        return self.currentAct


class Scenes:
    """
    This agent is responsible for managing the scenes.
    """

    def __init__(self, act):
        """
        This agent is responsible for managing the scenes.
        """
        self.act = act
        self.scenes = None
        self.sceneCount = None
        self.sceneIndex = None

        self.currentScene = None

        self.cue = None

        self.load()

    def load(self):
        """
        Loads the scenes from the act.
        """
        self.scenes = self.act.get("scenes")
        self.sceneCount = len(self.scenes)
        self.sceneIndex = 1
        self.currentScene = self.scenes[self.sceneIndex - 1]

        self.cue = Cues(self.get())

        return self.scenes

    def previous(self):
        """
        Returns the previous scene.
        """
        if self.sceneIndex > 1:
            self.sceneIndex -= 1
        else:
            self.sceneIndex = self.sceneCount
        return self.sceneIndex

    def next(self):
        """
        Returns the next scene.
        """
        if self.sceneIndex < self.sceneCount:
            self.sceneIndex += 1
        else:
            self.sceneIndex = 1
        return self.sceneIndex

    def get(self):
        """
        Returns the current scene.
        """
        return self.currentScene


class Cues:
    """
    This agent is responsible for managing the cues.
    """

    def __init__(self, act):
        """
        This agent is responsible for managing the cues.
        """
        self.act = act
        self.cues = None
        self.cueCount = None
        self.cueIndex = None

        self.currentCue = None
        self.load()

    def load(self):
        """
        Loads the cues from the act.
        """
        self.cues = self.act.get("cues")

        self.cueCount = len(self.cues)
        self.cueIndex = 1
        self.currentCue = self.cues[self.cueIndex - 1]
        return self.cues

    def previous(self):
        """
        Returns the previous cue.
        """
        if self.cueIndex > 1:
            self.cueIndex -= 1
        else:
            self.cueIndex = self.cueCount
        return self.cueIndex

    def next(self):
        """
        Returns the next cue.
        """
        if self.cueIndex < self.cueCount:
            self.cueIndex += 1
        else:
            self.cueIndex = 1
        return self.cueIndex

    def get(self):
        """
        Returns the current cue.
        """
        return self.currentCue


show = ShowAgent()


show.select("addams-family")

print(show.act.scene.cue.get())

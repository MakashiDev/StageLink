import os
import json


class ShowFile:
    SHOWS_FOLDER = "shows"

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.slug = name.lower().replace(" ", "-")
        self.id = 1  # Initialize ID
        self.actCount = 0
        self.currentAct = 1
        self.acts = []

    def add_act(self, act_number):
        if 1 <= act_number <= self.actCount + 1:
            new_act = {
                "act": act_number,
                "scenes": [],
            }
            self.acts.insert(act_number - 1, new_act)
            self.actCount += 1

            # Update act numbers for existing acts
            for i, act in enumerate(self.acts):
                act["act"] = i + 1

            # Update IDs and slugs for acts and scenes
            self.update_ids_and_slugs()

    def add_scene(self, act_number, scene_name):
        act = self.get_act_by_number(act_number)
        if act:
            scene = {
                "name": scene_name,
                "scene": act["sceneCount"] + 1,
                "slug": f"{self.slug}_scene_{act['sceneCount'] + 1}",
                "cues": [],
            }
            act["scenes"].append(scene)
            act["sceneCount"] += 1

            # Update scene numbers for existing scenes
            for i, scene in enumerate(act["scenes"]):
                scene["scene"] = i + 1

            # Update IDs and slugs for scenes
            self.update_ids_and_slugs()

    def add_cue(self, act_number, scene_number, cue_name, cue_type="default"):
        act = self.get_act_by_number(act_number)
        if act:
            scene = self.get_scene_by_number(act, scene_number)
            if scene:
                cue = {
                    "name": cue_name,
                    "slug": f"{self.slug}_scene_{scene['scene']}_cue_{scene['cueCount'] + 1}",
                }
                if cue_type != "default":
                    cue["type"] = cue_type

                scene["cues"].append(cue)
                scene["cueCount"] += 1

                # Update IDs and slugs for cues
                self.update_ids_and_slugs()

    def get_act_by_number(self, act_number):
        for act in self.acts:
            if act["act"] == act_number:
                return act
        return None

    def get_scene_by_number(self, act, scene_number):
        for scene in act["scenes"]:
            if scene["scene"] == scene_number:
                return scene
        return None

    def update_ids_and_slugs(self):
        self.id = 1
        for act in self.acts:
            act["id"] = self.id
            act["slug"] = f"{self.slug}_act_{self.id}"
            self.id += 1

            for scene in act["scenes"]:
                scene["slug"] = f"{act['slug']}_scene_{scene['scene']}"

    def __str__(self):
        return str({
            "name": self.name,
            "type": self.type,
            "slug": self.slug,
            "id": self.id,
            "actCount": self.actCount,
            "currentAct": self.currentAct,
            "acts": self.acts
        })

    def save_to_file(self):
        print("Saving show to file...")
        show_data = {
            "name": self.name,
            "type": self.type,
            "slug": self.slug,
            "id": self.id,
            "actCount": self.actCount,
            "currentAct": self.currentAct,
            "acts": self.acts
        }

        # Ensure the shows folder exists
        if not os.path.exists(self.SHOWS_FOLDER):
            os.makedirs(self.SHOWS_FOLDER)

        file_name = os.path.join(self.SHOWS_FOLDER, f"{self.slug}.json")
        print(f"Saving to {file_name}")

        with open(file_name, "w") as file:
            json.dump(show_data, file, indent=4)

        print("Show saved.")

    @classmethod
    def load_from_file(cls, slug):
        file_name = os.path.join(cls.SHOWS_FOLDER, f"{slug}.json")
        if not os.path.exists(file_name):
            return None

        with open(file_name, "r") as file:
            show_data = json.load(file)

        show = cls(show_data["name"], show_data["type"])
        show.slug = show_data["slug"]
        show.id = show_data["id"]
        show.actCount = show_data["actCount"]
        show.currentAct = show_data["currentAct"]
        show.acts = show_data["acts"]

        return show

    def edit_show(self, name=None, type=None):
        if name:
            self.name = name
            self.slug = name.lower().replace(" ", "-")
        if type:
            self.type = type

    def edit_act(self, act_number, new_act_number=None):
        act = self.get_act_by_number(act_number)
        if act:
            if new_act_number is not None:
                if 1 <= new_act_number <= self.actCount and new_act_number != act_number:
                    self.acts.insert(new_act_number - 1,
                                     self.acts.pop(act_number - 1))
                else:
                    return  # Invalid new act number

            # Update act numbers for existing acts
            for i, act in enumerate(self.acts):
                act["act"] = i + 1

            # Update IDs and slugs for acts and scenes
            self.update_ids_and_slugs()

    def edit_scene(self, act_number, scene_number, new_scene_name=None):
        act = self.get_act_by_number(act_number)
        if act:
            scene = self.get_scene_by_number(act, scene_number)
            if scene:
                if new_scene_name:
                    scene["name"] = new_scene_name
            else:
                print(
                    f"Scene {scene_number} in Act {act_number} does not exist.")
        else:
            print(f"Act {act_number} does not exist.")

    def edit_cue(self, act_number, scene_number, cue_number, new_cue_name=None, new_cue_type=None):
        act = self.get_act_by_number(act_number)
        if act:
            scene = self.get_scene_by_number(act, scene_number)
            if scene:
                if cue_number <= scene["cueCount"]:
                    cue = scene["cues"][cue_number - 1]
                    if new_cue_name:
                        cue["name"] = new_cue_name
                    if new_cue_type is not None:
                        cue["type"] = new_cue_type
                else:
                    print(
                        f"Cue {cue_number} does not exist in Scene {scene_number} of Act {act_number}.")
            else:
                print(
                    f"Scene {scene_number} does not exist in Act {act_number}.")
        else:
            print(f"Act {act_number} does not exist.")


# Example usage for Camp Rock
show = ShowFile("Camp Rock", "Musical")
show.add_act(1)
show.add_scene(1, "Camp Rock")
show.add_cue(1, 1, "Camp Rock")
show.add_cue(1, 1, "Camp Rock 2")
show.add_cue(1, 1, "Camp Rock 3")
show.add_scene(1, "Camp Star")
show.add_cue(1, 2, "Camp Star")
show.add_cue(1, 2, "Camp Star 2")
show.add_cue(1, 2, "Camp Star 3")
show.add_act(2)
show.add_scene(2, "Camp Rock")
show.add_cue(2, 1, "Camp Rock")
show.add_cue(2, 1, "Camp Rock 2")
show.add_cue(2, 1, "Camp Rock 3")
show.add_scene(2, "Camp Star")
show.add_cue(2, 2, "Camp Star")
show.add_cue(2, 2, "Camp Star 2")
show.add_cue(2, 2, "Camp Star 3")
show.save_to_file()

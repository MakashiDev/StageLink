class ShowFileGenerator {
	constructor(name, type) {
		const slug = this.slugify(name);
		this.show = {
			name,
			type,
			slug,
			acts: [],
		};
	}

	slugify(name) {
		return name.toLowerCase().replace(" ", "-");
	}

	addAct(actName) {
		const act = {
			name: actName,
			scenes: [],
		};
		this.show.acts.push(act);
	}

	addScene(actIndex, sceneName) {
		const scene = {
			name: sceneName,
			cues: [],
		};
		this.show.acts[actIndex].scenes.push(scene);
	}

	addCue(actIndex, sceneIndex, cueName, cueType) {
		const cue = {
			name: cueName,
			type: cueType,
		};
		this.show.acts[actIndex].scenes[sceneIndex].cues.push(cue);
	}

	getShow() {
		return this.show;
	}
}

// Example usage:
const myShowGenerator = new ShowFileGenerator(
	"Camp Rock",
	"Musical",
	"camp-rock"
);
myShowGenerator.addAct("Act 1");
myShowGenerator.addScene(0, "Camp Rock");
myShowGenerator.addCue(0, 0, "This Is Me", "Sound");
myShowGenerator.addCue(0, 0, "Mitchie Enters", "Stage");
myShowGenerator.addCue(0, 0, "Mitchie Sings", "Sound");
myShowGenerator.addCue(0, 0, "Mitchie Exits", "Stage");
myShowGenerator.addScene(0, "Camp Star");
myShowGenerator.addCue(0, 1, "Camp Star Enters", "Stage");
myShowGenerator.addCue(0, 1, "Camp Star Sings", "Sound");
myShowGenerator.addCue(0, 1, "Camp Star Exits", "Stage");
myShowGenerator.addAct("Act 2");
myShowGenerator.addScene(1, "Camp Rock");
myShowGenerator.addCue(1, 0, "Camp Rock Enters", "Stage");
myShowGenerator.addCue(1, 0, "Camp Rock Sings", "Sound");
myShowGenerator.addCue(1, 0, "Camp Rock Exits", "Stage");
myShowGenerator.addCue(1, 0, "Blackout", "Lighting");
myShowGenerator.addScene(1, "Camp Star");
myShowGenerator.addCue(1, 1, "Camp Star Enters", "Stage");
myShowGenerator.addCue(1, 1, "Camp Star Sings", "Sound");
myShowGenerator.addCue(1, 1, "Camp Star Exits", "Stage");
myShowGenerator.addAct("Act 3");
myShowGenerator.addScene(1, "Final Jam");
myShowGenerator.addCue(1, 0, "Final Jam Begins", "Stage");

const showFile = myShowGenerator.getShow();
console.log(JSON.stringify(showFile, null, 2));

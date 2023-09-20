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
myShowGenerator.addAct("Act 2");
myShowGenerator.addScene(1, "Final Jam");
myShowGenerator.addCue(1, 0, "Final Jam Begins", "Stage");

const showFile = myShowGenerator.getShow();
console.log(JSON.stringify(showFile, null, 2));

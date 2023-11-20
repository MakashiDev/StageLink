/**
 * Error Handling
 */

class ShowNotFound extends Error {
	/**
	 * Creates an instance of ShowNotFound.
	 * @param {string} slug - The slug of the show that was not found.
	 */
	constructor(slug) {
		super(`Show not found, ${slug} does not exist.`);
		this.name = "ShowNotFound";
		this.slug = slug;
		displayError(
			"Show Not Found",
			`The show ${slug} could not be found.`,
			`ShowNotFound: ${this.message}`
		);
	}
}

class ErrorLoadingShow extends Error {
	/**
	 * Creates an instance of ErrorLoadingShow.
	 * @param {string} slug - The slug of the show that was not found.
	 * @param {string} error - The error that was thrown.
	 * @param {string} message - The error message.
	 */
	constructor(slug, error, message) {
		super(
			`Error loading show, ${slug} could not be loaded. ${error}: ${message}`
		);
		this.name = "ErrorLoadingShow";
		this.slug = slug;
		this.error = error;
		this.message = message;
		displayError(
			"Error Loading Show",
			`The show ${slug} could not be loaded.`,
			`ErrorLoadingShow: ${this.message}`
		);
	}
}

class CueOutOfRange extends Error {
	/**
	 * Creates an instance of CueOutOfRange.
	 * @param {string} cue - The name of the cue that was not found.
	 * @param {number} cueIndex - The index of the cue.
	 * @param {number} cueCount - The total number of cues in the scene.
	 */
	constructor(cueIndex, cueCount) {
		super(
			`Cue not found, ${cueIndex} is out of range. There are ${cueCount} cues in this scene.`
		);

		this.name = "CueOutOfRange";
		this.cueIndex = cueIndex;
		this.cueCount = cueCount;
		displayError(
			"Cue Not Found",
			`The cue ${cueIndex} could not be found.`,
			`CueOutOfRange: ${this.message}`
		);
	}
}

function displayError(title, message, error, showButton = true) {
	let errorTitle = document.getElementById("error-title");
	let errorMessage = document.getElementById("error-message");
	let errorDetails = document.getElementById("error-details");

	errorTitle.innerText = title;
	errorMessage.innerText = message;
	errorDetails.innerText = error;

	let errorDiv = document.getElementById("error");
	errorDiv.classList.remove("!hidden");

	let errorClose = document.getElementById("error-close");
	if (!showButton) {
		errorClose.classList.add("!hidden");
	} else {
		errorClose.classList.remove("!hidden");
	}
	errorClose.addEventListener("click", () => {
		errorDiv.classList.add("!hidden");
		// go to home page
		window.location.href = "/";
	});
}

/**
 * Acts Class
 */
class Acts {
	/**
	 * Creates an instance of Acts.
	 * @param {object} show - The show object.
	 */
	constructor(show) {
		this.show = show;
		this.actIndex = null;
		this.currentAct = null;
		this.actCount = null;
		this.scene = null;
		this.load();
	}

	/**
	 * Load the initial act and scene.
	 */
	load() {
		this.acts = this.show.acts;
		this.actCount = this.acts.length;
		this.actIndex = 1;
		this.currentAct = this.acts[this.actIndex - 1];
		this.scene = new Scenes(this.get());
	}

	/**
	 * Navigate to the previous act.
	 * @returns {number} - The index of the previous act.
	 */
	previous() {
		if (this.actIndex > 1) {
			this.actIndex -= 1;
		} else {
			this.actIndex = this.actCount;
		}
		this.currentAct = this.acts[this.actIndex - 1];
		this.scene = new Scenes(this.get());
		return this.currentAct;
	}

	/**
	 * Navigate to the next act.
	 * @returns {number} - The index of the next act.
	 */
	next() {
		if (this.actIndex < this.actCount) {
			this.actIndex += 1;
		} else {
			this.actIndex = 1;
		}
		this.currentAct = this.acts[this.actIndex - 1];
		this.scene = new Scenes(this.get());
		return this.currentAct;
	}

	/**
	 * Get the current act.
	 * @returns {object} - The current act object.
	 */
	get() {
		return this.currentAct;
	}
}

/**
 * Scenes Class
 */
class Scenes {
	/**
	 * Creates an instance of Scenes.
	 * @param {object} act - The act object.
	 */
	constructor(act) {
		this.act = act;
		this.scenes = null;
		this.sceneCount = null;
		this.sceneIndex = null;
		this.currentScene = null;
		this.cue = null;
		this.load();
	}

	/**
	 * Load the initial scene and cues.
	 */
	load() {
		this.scenes = this.act.scenes;
		this.sceneCount = this.scenes.length;
		this.sceneIndex = 1;
		this.currentScene = this.scenes[this.sceneIndex - 1];
		this.cue = new Cues(this.get());
	}

	/**
	 * Navigate to the previous scene.
	 * @returns {number} - The index of the previous scene.
	 */
	previous() {
		if (this.sceneIndex > 1) {
			this.sceneIndex -= 1;
		} else {
			this.sceneIndex = this.sceneCount;
		}
		this.currentScene = this.scenes[this.sceneIndex - 1];
		this.cue = new Cues(this.get());
		return this.currentScene;
	}

	/**
	 * Navigate to the next scene.
	 * @returns {number} - The index of the next scene.
	 */
	next() {
		if (this.sceneIndex < this.sceneCount) {
			this.sceneIndex += 1;
		} else {
			this.sceneIndex = 1;
		}
		this.currentScene = this.scenes[this.sceneIndex - 1];
		this.cue = new Cues(this.get());
		return this.currentScene;
	}

	/**
	 * Get the current scene.
	 * @returns {object} - The current scene object.
	 */
	get() {
		return this.currentScene;
	}
}

/**
 * Cues Class
 */
class Cues {
	/**
	 * Creates an instance of Cues.
	 * @param {object} act - The act object.
	 */
	constructor(act) {
		this.act = act;
		this.cues = null;
		this.cueCount = null;
		this.cueIndex = null;
		this.currentCue = null;
		this.CueOutOfRange = CueOutOfRange;
		this.load();
	}

	/**
	 * Load the initial cues.
	 */
	load() {
		this.cues = this.act.cues;
		this.cueCount = this.cues.length;
		this.cueIndex = 1;
		this.currentCue = this.cues[this.cueIndex - 1];
		this.updateCueList();
	}

	/**
	 * Navigate to the previous cue.
	 * @returns {number} - The index of the previous cue.
	 */
	previous() {
		if (this.cueIndex > 1) {
			this.cueIndex -= 1;
			this.cue = this.cues[this.cueIndex - 1];
		} else {
			// Cue not found
			throw new this.CueOutOfRange(this.cueIndex - 1, this.cueCount);
		}
		this.currentCue = this.cues[this.cueIndex - 1];
		this.unselectCue(this.cueIndex + 1);
		this.selectCue(this.cueIndex);
		return this.cueIndex;
	}

	/**
	 * Navigate to the next cue.
	 * @returns {number} - The index of the next cue.
	 */
	next() {
		if (this.cueIndex < this.cueCount) {
			this.cueIndex += 1;
			this.cue = this.cues[this.cueIndex - 1];
		} else {
			// Cue not found
			throw new this.CueOutOfRange(this.cueIndex + 1, this.cueCount);
		}
		this.currentCue = this.cues[this.cueIndex - 1];
		this.unselectCue(this.cueIndex - 1);
		this.selectCue(this.cueIndex);
		return this.cueIndex;
	}

	/**
	 * Get all cues.
	 * @returns {object} - All cue objects.
	 * @todo - Add a filter to get only cues with a certain type.
	 * @todo - Add a filter to get only cues with a certain name.
	 * @todo - Add a filter to get only cues with a certain index.
	 */
	getAll() {
		return this.cues;
	}

	updateCueList() {
		let cueList = document.getElementById("cue-list");
		let cues = this.getAll();

		const baseCueClasses = "flex justify-between items-center w-full px-5";

		const stageCueClasses = "bg-purple-500 bg-opacity-50";
		const stageCueIconClasses = "la la-route";

		const soundCueClasses = "bg-red-500 bg-opacity-50";
		const soundCueIconClasses = "las la-microphone-alt";

		const lightCueClasses = "bg-green-500 bg-opacity-50";
		const lightCueIconClasses = "las la-lightbulb";

		cueList.innerHTML = "";
		cues.forEach((cue) => {
			let cueItem = document.createElement("li");

			let span = document.createElement("span");
			span.innerHTML = cue.name;
			cueItem.appendChild(span);

			let icon = document.createElement("i");

			cueItem.className = baseCueClasses;
			switch (cue.type.toLowerCase()) {
				case "stage":
					cueItem.className += ` ${stageCueClasses}`;
					icon.className = stageCueIconClasses;
					break;
				case "sound":
					cueItem.className += ` ${soundCueClasses}`;
					icon.className = soundCueIconClasses;
					break;
				case "lighting":
					cueItem.className += ` ${lightCueClasses}`;
					icon.className = lightCueIconClasses;
					break;
				default:
					break;
			}

			cueItem.appendChild(icon);
			cueList.appendChild(cueItem);
		});

		this.selectCue(this.cueIndex);
	}

	selectCue(index) {
		console.log("selecting cue");
		console.log(index);
		this.currentCue = this.cues[index - 1];
		this.cueIndex = index;
		let cueList = document.getElementById("cue-list");
		let cues = cueList.getElementsByTagName("li");
		let cue = cues[index - 1];
		cue.className += " bg-opacity-80";
	}

	unselectCue(index) {
		console.log("unselecting cue");
		console.log(index);
		let cueList = document.getElementById("cue-list");
		let cues = cueList.getElementsByTagName("li");
		let cue = cues[index - 1];

		cue.className = cue.className.replace(" bg-opacity-80", "");
	}

	/**
	 * Get the current cue.
	 * @returns {object} - The current cue object.
	 */
	get() {
		return this.currentCue;
	}
}

/**
 * Show Class
 */
class Show {
	/**
	 * Creates an instance of Show.
	 */
	constructor() {
		this.slug = null;
		this.show = null;
		this.name = null;
		this.type = null;
		this.acts = null;
	}

	/**
	 * Load a show from a file.
	 * @param {object} showFile - The show object from a file.
	 */
	load(showFile) {
		try {
			console.log(showFile);
			this.show = showFile; // Load the show object
			this.name = this.show.name;
			this.type =
				this.show.type[0].toUpperCase() + this.show.type.slice(1);
			this.slug = this.show.slug;
			this.showType = this.show.type;
			this.acts = new Acts(this.show);
		} catch (error) {
			throw new ErrorLoadingShow(this.slug, error.name, error.message);
		}
	}

	/**
	 * Load a show from the web.
	 * @param {string} slug - The slug of the show to load from the web.
	 */
	async loadFromWeb(slug) {
		let showFile = await fetch(`/api/show/${slug}`);
		showFile = await showFile.json();
		this.load(showFile);
		return this.show;
	}

	/**
	 * Update the show's data.
	 */
	update() {
		socket.emit(`update`, this.show);
	}

	next() {
		if (this.acts.scene.cue.cueIndex < this.acts.scene.cue.cueCount) {
			this.acts.scene.cue.next();
		} else if (this.acts.scene.sceneIndex < this.acts.scene.sceneCount) {
			this.acts.scene.next();
		} else if (this.acts.actIndex < this.acts.actCount) {
			this.acts.next();
		} else {
			this.acts.load();
		}
	}
}

// Show Info
const showName = document.getElementById("show-title");
const showType = document.getElementById("show-type");
const showAct = document.getElementById("show-act");
const showScene = document.getElementById("show-scene");

// Buttons
const goButton = document.getElementById("goButton");
const standbyButton = document.getElementById("standbyButton");
const stopButton = document.getElementById("stopButton");

// show_slug varible is defined in html file same with socket
const show = new Show(); // Create a new show
const selectedShow = show.loadFromWeb(show_slug).then((result) => {
	console.log("SHOW LOADED BBG");
	showName.innerText = show.name;
	showType.innerText = show.type;
	showAct.innerText = `Act ${show.acts.actIndex}`;
	showScene.innerText = `Scene ${show.acts.scene.sceneIndex}`;
	console.log(show.acts.scene.cue.getAll());
});

// Event Listeners
goButton.addEventListener("click", () => {
	show.next();
});

standbyButton.addEventListener("click", () => {
	console.log("standby");
	socket.emit("standby");
});

stopButton.addEventListener("click", () => {
	socket.emit("stop");
});

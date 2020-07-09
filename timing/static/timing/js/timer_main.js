var btn = document.getElementById("startPauseBtn");  //vars kinda required here, not lets
var resBtn = document.getElementById("resetBtn");
var slider = document.getElementById("slider");
var output = document.getElementById("output");  //time for the exercise goes here
var workoutName = document.getElementById("wrk-name");  //name of the exercise goes here

var timings = findForPlay();  //loading names and durations of exercises
var running = 0;  //flag
var j = 0;  //identifier for current exercise, starts from 0
var time = setInitTime();  //current time, multiplied by 10 cause it's measured in 100ms per tick
//var clingSound = new Audio('/static/timing/sounds/end_sound.wav');  //sound when exercise changes

function startPause(){
    workoutName.style.background = getBackColor(timings[j]);
	if(running == 0){
		running = 1;
		decrement();
		btn.innerHTML = "Pause";
	}else{
		running = 0;
		btn.innerHTML = "Resume";
	}
};

function reset(){
    j = 0;  //setting identifier for the first element here too
    initializeTimer();
    running = 0;
    workoutName.style.background = getBackColor(timings[j]);
	btn.innerHTML = "Start";
};

function decrement(){
	if(running == 1){
		setTimeout(function(){
            time--;
            if (time <= 0) {
                running = 0;
                output.innerHTML = "00:00";
                slider.style.width = 0 + "%";
                j++;
                if (timings[j][1] != undefined){
                    time = timings[j][1]*10;
                    workoutName.innerHTML = timings[j][0]
                    startPause();
                    return null;
                }
                console.log('finish');
            }
			var mins = Math.floor(time / 10 / 60);
			if(mins <= 9){
				mins = "0" + mins;
			}
			var secs = Math.ceil(time / 10);
			if(secs <= 9){
				secs = "0" + secs;
			}
			slider.style.width = time/timings[j][1]*10 + "%";
			output.innerHTML = mins + ":" + secs;
			decrement();
		}, 100);
	}
};

function initializeTimer() {
    time = setInitTime();
    let mins = Math.floor(time / 10 / 60);
    if(mins <= 9){
        mins = "0" + mins;
    }
    let secs = Math.ceil(time / 10);
    if(secs <= 9){
        secs = "0" + secs;
    }
    workoutName.innerHTML = timings[0][0];
    workoutName.style.background = getBackColor(timings[0]);
    output.innerHTML = mins + ":" + secs;
};

function setInitTime() {
    try {
        let inner = 0
        if (running){
        inner = timings[j][1]*10 + 1;  //choosing first element of timings again; plus 1 in order to escape 1 extra tick
        } else {
        inner = timings[j][1]*10;
        }
        return inner;
    }
    catch (e) {
        output.innerHTML = "00:00";
        workoutName.innerHTML = "No exercises yet";
        throw e;
    }
}

function getBackColor(timingInstance) {
    if (timingInstance[2] === 'exercise') {  //it is what it is
        return 'green';
    }
    else if (timingInstance[2] === 'break') {
        return 'orange';
    }
    else if (timingInstance[2] === 'warmup') {
        return 'yellow';
    }
    else if (timingInstance[2] === 'cooldown') {
        return 'blue';
    }
}

initializeTimer();
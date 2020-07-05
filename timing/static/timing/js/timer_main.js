var btn = document.getElementById("startPauseBtn");
var resBtn = document.getElementById("resetBtn");
var slider = document.getElementById("slider");
var output = document.getElementById("output");

var timings = [5, 2, 3];
var running = 0;
var j = 0;
var time = timings[0]*10;

function startPause(){
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
	running = 0;
    time = timings[0]*10;
    j = 0;
	output.innerHTML = "00:00";
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
                if (timings[j] != undefined){
                    time = timings[j]*10;
                    startPause();
                    return null;
                }
                console.log('finish');
            }
			var mins = Math.floor(time / 10 / 60);
			if(mins <= 9){
				mins = "0" + mins;
			}
			var secs = Math.floor(time / 10);
			if(secs <= 9){
				secs = "0" + secs;
			}
			slider.style.width = time/timings[j] *10 + "%"
			output.innerHTML = mins + ":" + secs;
			decrement();
		}, 100);
	}
};

function initializeTimer() {
    let mins = Math.floor(time / 10 / 60);
    if(mins <= 9){
        mins = "0" + mins;
    }
    let secs = Math.floor(time / 10);
    if(secs <= 9){
        secs = "0" + secs;
    }
    output.innerHTML = mins + ":" + secs;
};

initializeTimer();
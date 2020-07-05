var time = 100;
var running = 0;

//document.getElementById("output").innerHTML = Math.floor(secs / 10 / 60) + ":" + Math.floor(secs / 10) + ":00";

function startPause(){
	if(running == 0){
		running = 1;
		decrement();
		document.getElementById("startPause").innerHTML = "Pause";
	}else{
		running = 0;
		document.getElementById("startPause").innerHTML = "Resume";
	}
};

function reset(){
	running = 0;
	time = 50;
	document.getElementById("output").innerHTML = "00:00";
	document.getElementById("startPause").innerHTML = "Start";
};

function decrement(){
	if(running == 1){
		setTimeout(function(){
			time--;
			if (time <= 0) {
			    running = 0;
			    document.getElementById("output").innerHTML = "00:00";
			    return null
			}
			var mins = Math.floor(time / 10 / 60);
			if(mins <= 9){
				mins = "0" + mins;
			}
			var secs = Math.ceil(time / 10);
			if(secs <= 9){
				secs = "0" + secs;
			}
			document.getElementById("output").innerHTML = mins + ":" + secs;
			decrement();
		}, 100);
	}
};
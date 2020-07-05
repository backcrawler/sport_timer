var fps = 60;

var Timer = function(obj){  //main Timer "class"
  this.time = obj.time;  //the time to count
  this.fps = obj.fps;
  this.onEnd = obj.onEnd || null;
  this.onStart = obj.onStart || null;
  this.intervalID = null;

  this.start = () => {
    this.startTime = this.time
    this.interval = setInterval(this.update, 1000 / this.fps);
    this.onStart ? this.onStart() : void 0;
    return this;
  };
  this.stop = () => {
    clearInterval(this.interval);
    this.onEnd ? this.onEnd() : void 0;
  };
  this.onTick = () => {
    id("output").innerHTML = this.get("dig");
    id("slider").style.width = this.get()/this.startTime *100 + "%";
  }
  this.update = () => {
    this.time > 0 ? this.time -= 1/this.fps : this.stop(); // either continue or stop the timer
    this.onTick ? this.onTick() : void 0;
    return this.get();
  }
  this.get = (par) => {
    switch(par) {
      case undefined:
        return this.time;
        break;
      case "dig":
        return Math.ceil(this.time);
        break;
      case "end":
        return this.onEnd();
        break;
    }
  }
}

function onTimerStart(){
  console.log("timer started");
}
function endTimer(){
  console.log("timer ended");
}

function id(id){
  return document.getElementById(id);
}

let timers = [];
let info = [4,10,3,2,1,0,5];
info.forEach(element => {
    let curTimer = new Timer({
      time: element,
      fps: fps,
      onEnd: endTimer,
      onStart: onTimerStart
    });
    timers.push(curTimer);
});

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
};

const doTiming = async () => {
  for (let x of timers) {
    let sleepTime = x.time;
    x.start();
    requestAnimationFrame(x.onTick);
    await sleep(x.time*1000);
  }
};

function startTimer(seconds, container, oncomplete) {
    var startTime, timer, obj, ms = seconds*1000,
        display = document.getElementById(container),
        pausingBtn = document.getElementById('pausing_btn'),
        resumeBtn = document.getElementById('resuming_btn');
    obj = {};
    obj.resume = function() {
        startTime = new Date().getTime();
        timer = setInterval(obj.step,250); // adjust this number to affect granularity
                            // lower numbers are more accurate, but more CPU-expensive
    };
    obj.pause = function() {
        ms = obj.step();
        clearInterval(timer);
    };
    pausingBtn.onclick = obj.pause;
    resumeBtn.onclick = obj.resume();
    obj.step = function() {
        var now = Math.max(0,ms-(new Date().getTime()-startTime)),
            m = Math.floor(now/60000), s = Math.floor(now/1000)%60;
        s = (s < 10 ? "0" : "")+s;
        display.innerHTML = m+":"+s;
        if( now == 0) {
            clearInterval(timer);
            obj.resume = function() {};
            if( oncomplete) oncomplete();
        }
        return now;
    };
    obj.resume();
    return obj;
}

var timer = startTimer(10, "output", function() {alert("Done!");});
//var timer2 = startTimer(2, "output", function() {alert("Done2!");});
//doTiming();
let btn = document.getElementById("startPauseBtn");
let resBtn = document.getElementById("resetBtn");
let output = document.getElementById("output");

let Timer = function(obj){  //main "class" object
    this.initTime = obj.time;  //initial time in 0.1 of seconds, doesn't change
    this.onEnd = obj.onEnd || null;  //callback executed at the end of the timer
    this.started = false;  //whether the timer has been started before or it's the 1st time
    this.running = 0;  //flag for state

    this.onStart = () => {
        if (this.started){
            null;
        }
        else {
            let mins = Math.floor(this.time / 10 / 60);
            if(mins <= 9){
                mins = "0" + mins;
            }
            let secs = Math.ceil(this.time / 10);
            if(secs <= 9){
                secs = "0" + secs;
            }
            output = mins + ":" + secs
            this.started = true;
            this.running = 0;  // so it will be reversed in startPause
            this.time = this.initTime;  //resetting
            resBtn.onclick = this.reset;
        }
    };
    this.startPause = () => {
        console.log('timer started')
        this.onStart();
        if(this.running == 0){
            this.running = 1;
            this.decrement();
            console.log('counting')
            btn.innerHTML = "Pause";
        }
        else{
            this.running = 0;
            btn.innerHTML = "Resume";
        }
        btn.onclick = this.startPause;
    };
    this.reset = () => {
        this.started = false;
        this.running = 0;
        btn.innerHTML = "Resume";
        btn.onclick = master.startPause;
    };
    this.decrement = () => {
        console.log('inside decrement')
        if(this.running == 1){
            setTimeout( ()=> {
                this.time--;
                if (this.time <= 0) {
                    this.running = 0;
                    this.started = false;
                    output.innerHTML = "00:00";
                    console.log('timer ended')
                    if (this.onEnd){
                        return this.onEnd();
                    }
                    else {
                        return null;
                    }

                }
                let mins = Math.floor(this.time / 10 / 60);
                if(mins <= 9){
                    mins = "0" + mins;
                }
                let secs = Math.ceil(this.time / 10);
                if(secs <= 9){
                    secs = "0" + secs;
                }
                output.innerHTML = mins + ":" + secs;
                console.log(this.time);
                console.log(this.started);
                console.log(this.onStart);
                this.decrement();
            }, 100);
        }
    };
}

//test
let timers = [];
let info = [['First', 5], ['Second', 3], ['Third', 7]];
for (let i=0; i<info.length; i++) {
    first = info[i];
    second = info[i+1];
    if (i === 0) {
        let master = new Timer({
            initTime: first
        });
        btn.onclick = master.startPause;
        timers.push(master);
    }
    if (second) {
        let curTimer = new Timer({
            initTime: second
        });
        timers[timers.length-1].onEnd = curTimer.startPause;
        timers.push(curTimer);
    }
}
console.log('Timers initialized')
let master = timers[0]
resBtn.onclick = master.reset;
btn.onclick = master.startPause;
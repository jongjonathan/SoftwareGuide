function clock() {
    var clocker = new Date();

    var hours = clocker.getHours();
    var minutes = clocker.getMinutes();
    var seconds = clocker.getSeconds();

    var amPm = (hours<12)? "AM" : "PM";

    hours = (hours>12) ? hours - 12: hours;
    hours = ("0" + hours).slice(-2);
    minutes = ("0"+ minutes).slice(-2);
    seconds = ("0" + seconds).slice(-2);

    document.getElementById('clock').innerHTML = hours + " : " + minutes + " : " + seconds + " " + amPm;
    var t = setTimeout(clock, 500);


}
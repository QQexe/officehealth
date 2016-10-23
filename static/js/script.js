var goods = ["better air quality", "reduced noise levels", "balanced lighting", "happier employees", "reduced stress", "healthier lifestyles"];

var text = document.getElementById('goodtext');

function iterateMessages() {
    window.alert("!");
    var num = 0;
    window.setInterval(function () {
        text.innerHTML = "Performance through " + goods[num];
        if (num >= goods.length) {
            num = 0;
        }
    }, 3000);
}

window.alert("1");

window.onload = iterateMessages;

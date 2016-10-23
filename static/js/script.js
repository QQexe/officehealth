var goods = ["better air quality", "reduced noise levels", "balanced lighting", "happier employees", "reduced stress", "healthier lifestyles"];

text = document.getElementById('goodtext');

window.onload = function start() {
    iterateMessages();
}
function iterateMessages() {
    var num = 0,
    window.setInterval(function () {
        text = goods[num];
        if (num >= goods.length) {
            num = 0
        }
    }, 3000);
}

for (i = 0; i < goods.length; i++) {
    text = goods[i];
}
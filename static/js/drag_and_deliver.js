
window.onload = function(){
    const chessblock = document.querySelectorAll('.chessblock');
    for (var square of chessblock){
        square.addEventListener('dragstart', drag);
        }
    }


function drag(ev){
    ev.dataTransfer.setData("text/plain", ev.target.id);
    var legalist = document.getElementById("legalist").innerHTML.split(",");
    for (var square of chessblock){
        if (legalist.includes(ev.dataTransfer.getData("text/plain").substring(0,2) + square.id.substring(2))){
            square.style.backgroundColor="#008000"
            }
        }
}


function drop(ev){
    
    var data = ev.dataTransfer.getData("text");
}
function allowDrop(ev) {
    ev.preventDefault();
  }
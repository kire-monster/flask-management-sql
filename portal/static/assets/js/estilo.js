var jsMenu = (function(){
    var mostrarMenu = function(elem){
        var x = elem.parentNode
        if (x.className === "topnav") {x.className += " responsive";}
        else {x.className = "topnav";}
    }
    return {show: mostrarMenu}
})()
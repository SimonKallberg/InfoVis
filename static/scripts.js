// JavaScript for label effects only


var stat2 = function() {
		localStorage.setItem('selectedtem', document.getElementById("stat2").value);
		console.log(localStorage.getItem("selectedtem"));
};

window.onload = function(){
	if (localStorage.getItem('selectedtem')) {
		console.log(localStorage.getItem("selectedtem"));
		document.getElementById("stat2").value = localStorage.getItem('selectedtem');
	}

		//
};

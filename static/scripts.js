// JavaScript for label effects only, can use for loops but coded each one since it is so few
function checkstat1(){
		localStorage.setItem('selectedStat1', document.getElementById("stat1").value);
};

function checkstat2(){
		localStorage.setItem('selectedStat2', document.getElementById("stat2").value);
};

function checkstat3(){
		localStorage.setItem('selectedStat3', document.getElementById("stat3").value);
};

function checkstat4(){
		localStorage.setItem('selectedStat4', document.getElementById("stat4").value);
};

function checkstat5(){
		localStorage.setItem('selectedStat5', document.getElementById("stat5").value);
};

function test(){
	console.log("test function");
}

window.onload = function(){
	console.log("HEJ");
	if (localStorage.getItem('selectedStat1')) {
		console.log(localStorage.getItem("selectedStat1"));
		document.getElementById("stat1").value = localStorage.getItem('selectedStat1');
	}
	if (localStorage.getItem('selectedStat2')) {
		console.log(localStorage.getItem("selectedStat2"));
		document.getElementById("stat2").value = localStorage.getItem('selectedStat2');
	}
	if (localStorage.getItem('selectedStat3')) {
		console.log(localStorage.getItem("selectedStat3"));
		document.getElementById("stat3").value = localStorage.getItem('selectedStat3');
	}
	if (localStorage.getItem('selectedStat4')) {
		document.getElementById("stat4").value = localStorage.getItem('selectedStat4');
	}
	if (localStorage.getItem('selectedStat5')) {
		document.getElementById("stat5").value = localStorage.getItem('selectedStat5');
	}
};

nav_open = 0;

function open_close_nav () {
	
	nav = document.getElementById("nav_a");
	
	if (nav_open==0) {
		nav.style.visibility="visible";
		nav_open = 1;
	}else {
		nav.style.visibility="hidden";
		nav_open = 0;
	}
}
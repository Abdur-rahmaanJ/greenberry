// Initialise sidenav trigger
$(document).ready(function () {
    $('.sidenav').sidenav();
});

$( ".change" ).on("click", function() {
  if( $( "body" ).hasClass( "dark" )) {
                $( "body" ).removeClass( "dark" );
              $( "div" ).addClass( "light" );
              $( "span" ).removeClass( "black" );
              document.getElementbyClassName("toggle").style.boxShadow = "none";
              }
  else{
   $( "body" ).addClass( "dark" );
   $( "span" ).addClass( "black" );
 }
});

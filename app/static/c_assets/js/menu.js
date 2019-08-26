$(function(){

	$(".menu").click(function(e) {
        var menu="<div id='menu'></div>";
		
		$("body").append(menu);
		
		$("#menu").html($("header .nav").html()+$("header .userBtn").html()+"<a class='closeMenu'>x</a>");
		$(".closeMenu").click(function(e) {
            $("#menu").remove();
        });
    });
	
	
	
	
});
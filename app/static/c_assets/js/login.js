// JavaScript Document
$(function(){

	$("#codeImg").click(function(e) {
		var src=$(this).attr("src");
		$(this).attr("src",src+"?");
	});


	$(".login_box").mousemove(function(e){
		//中心点
		var pointX=$(this).width()/2;
		var pointY=$(this).height()/2;
		
		var speed=5;
		var num=$(this).find(".login_bg div").length;
		
		var xbz=(pointX-e.clientX)/pointX;
		var ybz=(pointY-e.clientY)/pointY;
				
		$(this).find(".login_bg div").each(function(index,element){
			
			var nx=((index)*speed)*xbz;
			var ny=((index)*speed)*ybz;
			
			$(this).css("top",ny);
			$(this).css("left",nx);
			
		});
		
	});

});
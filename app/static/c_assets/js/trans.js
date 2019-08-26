// JavaScript Document
$(function(){
	
	$(".tranTab").mousemove(function(e){
		//中心点
		var pointX=$(this).width()/2;
		var pointY=$(this).height()/2;
		
		var speed=10;
		var num=$(this).find(".tranPics img").length;
		
		var xbz=(pointX-e.clientX)/pointX;
		var ybz=(pointY-e.clientY)/pointY;
				
		$(this).find(".tranPics img").each(function(index,element){
			
			var nx=((index+2)*speed)*xbz;
			var ny=((index+2)*speed)*ybz;
			
			$(this).css("top",ny);
			$(this).css("left",nx);
			
		});
		
	});




});
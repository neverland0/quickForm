$(document).ready(function(){
	$("ul").each(function(){
		if($(this).children().length > 3){
			$(this).children().replaceWith($(this).children().slice(0,2));
			$(this).append("<p>...</p>");
		}
		else if($(this).children().length < 3){
			n = 3 - $(this).children().length;
			if(n == 1){
				$(this).append("<li></li>");
			}else if(n == 2){
				$(this).append("<li></li><li></li>");
			}else if(n == 3){
				$(this).append("<li></li><li></li><li></li>");
			}
		}
	});
});
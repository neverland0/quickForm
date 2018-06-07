$(document).ready(function(){
	

	$(".div_item ul").each(function(){
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
	$(".div_item").hide();
	$("#food").show();
	$("#show_food").click(function(){
		$(".div_item").hide();
		$("#food").show();
	});
	$("#show_teach").click(function(){
		$(".div_item").hide();
		$("#teach").show();
	});
	$("#show_sold").click(function(){
		$(".div_item").hide();
		$("#sold").show();
	});
	$("#show_web").click(function(){
		$(".div_item").hide();
		$("#web").show();
	});
});
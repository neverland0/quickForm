$(document).ready(function(){
	var choice_copy;
	$(".btn_close").click(function(){

		a = $(this).parents(".div_question").siblings().filter(".div_question").length;
		if(a>0)
		{
			//$(this).parents(".div_question").remove();
			$(this).parents(".div_question").animate({ opacity:'0.1' }, 500,function(){
				$(this).remove()
			});
		}

	});
	$(".get_back").hide();
	$(".div_blank").hide();
	$(".kind").bind("change",function(){
		
		var list = $(this).parents(".div_question").find(".div_content").children();
		choice = list.filter(".div_choice");
		
		blank = list.filter(".div_blank");
		switch($(this).val()){
			case "single":
			choice.show();
			blank.hide();
			if(choice.find("div").children().first().hasClass("glyphicon-record"))
			{

			}
			else
			{
				choice.find(".glyphicon-unchecked").addClass("glyphicon-record");	
				choice.find(".glyphicon-unchecked").removeClass("glyphicon-unchecked");
				
			}
			
			break;

			case "multi":
			
			choice.show();
			blank.hide();
			if(choice.find("div").children().first().hasClass("glyphicon-unchecked"))
			{

			}
			else
			{
				choice.find(".glyphicon-record").addClass("glyphicon-unchecked");
				choice.find(".glyphicon-record").removeClass("glyphicon-record");	
			}
			break;

			case "blank":
			choice.hide();
			
			blank.show();
			break;
		}
		choice_copy = $(".choice_item").clone(true);
	});
	$(".del_choice").click( function(){
		a = $(this).parents(".choice_item").siblings().filter(".choice_item").length;
		
		if(a>0)
		{
			$(this).parents(".choice_item").remove();
		}
	});	

	choice_copy = $(".choice_item").clone(true);
	
	$(".add_choice").click(function(){
		//$(this).before(choice_copy.clone(true));
		cp = $(this).prev().clone(true);
		cp.find("input").val("");
		$(this).before(cp);
		//$(this).parents()
	});


	question_copy = $(".div_question:eq(-1)").clone(true);
	$(".btn_add_question").click(function(){
		$(this).before(question_copy.clone(true));
		$(this).prev().find("#question_text").focus();
		$("html, body").animate({ scrollTop: $(document).height() }, 1000);
	});

	

	$(".btn_submit").click(function(){
		question_flag=false;
		choice_flag=false;
		same_flag=false;
		a = $(this).siblings().filter(".div_question");
		title = $(this).siblings().filter(".page-header").find("#title");

		
		var ques_nare = new Object();
		ques_nare.title = title.val();
		ques_nare.items = new Array();

		count = 1;
		a.each(function(){
			//alert($(this).find(".kind").val());
			var item = new Object();
			item.question = $(this).find("#question_text").val();
			if(item.question==null||item.question==''){
				question_flag=true;	
			}
			
			item.no = count;
			count++;
			item.kind = $(this).find(".kind").val();
			item.choice = new Array();
			if(item.kind == "single" || item.kind == "multi")
			{
				b = $(this).find(".choice_item");
				
				b.each(function(){
					c = $(this).find("#choice_text").val();
					if(c==null||c==''){
						choice_flag=true;
					}
					
					item.choice.push(c);
				});
				str_choice = item.choice.join(",");
				item.choice.forEach(function(value,index,array){
					if((str_choice.indexOf(value))!=(str_choice.lastIndexOf(value)))
					{
						same_flag=true;
					}
				});
			}
			ques_nare.items.push(item);
		});
		jsontext = JSON.stringify(ques_nare);
		if(question_flag){
			alert('问题不能为空');
		}
		else if(choice_flag){
			alert('选项不能为空');
		}
		else if(same_flag){
			alert('选项不能相同');
		}
		else{
			$.ajax({
			url : $SCRIPT_ROOT + '/design',
			type : 'POST',
			data : jsontext,
			success : function(result){
				str_url = $FEED_URL + result.result;//bug
				$(".get_back textarea").text(str_url);
				$("#cp").click(function(){
					e = document.getElementById("source_url");
					e.select();
					document.execCommand("Copy");
				});
				$(".get_back").toggle();

			//alert(result.result);
			}

		});
		}
		
		
	});
	
});
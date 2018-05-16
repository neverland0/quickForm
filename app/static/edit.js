$(document).ready(function(){
	$(".kind").change();
	question_copy = $(".div_question:eq(-1)").clone(true);
	$(".btn_add_question").unbind();
	$(".btn_add_question").click(function(){
		question_copy.find("#question_text").val("");
		
		question_copy.find("#kind").val("single");
		question_copy.find("#choice_text").val("");
		question_copy.find(".choice_item").replaceAll(question_copy.find(".choice_item").first());

		$(this).before(question_copy.clone(true));
		$(this).prev().find("#question_text").focus();
		$("html, body").animate({ scrollTop: $(document).height() }, 1000);
	});
});
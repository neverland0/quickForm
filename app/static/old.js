$(document).ready(function(){
	//alert($BASE_URL);
	$(function () {
  		$('[data-toggle="popover"]').popover()
	})
	$(".btn_close").click(function(){
		id = $(this).prev().text();
		a = new Object()
		a.id = id
		jsontext = JSON.stringify(a);
		th = $(this)
		$.ajax({
			url : $SCRIPT_ROOT + '/old/delete',
			type : 'POST',
			data : jsontext,
			success : function(result){
				//alert('ok')
				th.parents(".div_question").remove();
			}

		});
	});
	
});
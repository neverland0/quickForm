
$(document).ready(function(){
    $(".answer-list").children().each(function(){
        $(this).hide()
    });
    $(".answer-list").children().first().show();
    $(".previous a").click(function(event){
        event.preventDefault();
        active = $(".answer-list > div:visible");
        if(active.prev().is("div")){
            active.prev().show();
            active.hide();    
        }
        
    });
    $(".next a").click(function(event){
        event.preventDefault();
        active = $(".answer-list > div:visible");
        if (active.next().is("div")) {
            active.next().show();
            active.hide();    
        }
        
    });
});


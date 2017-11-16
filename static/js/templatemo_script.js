
    
$(document).ready( function() {        

	// sidebar menu click
	$('.templatemo-sidebar-menu li.sub a').click(function(){
		if($(this).parent().hasClass('open')) {
			$(this).parent().removeClass('open');
		} else {
			$(this).parent().addClass('open');
		}
	});  // sidebar menu click

	$('.form-group .logininput input').addClass('form-control');

    $(".templatemo-sidebar .templatemo-sidebar-menu >li a").each(function(){
        console.log($(this).attr("href"))
        var url = window.location.pathname;
        if($(this).attr("href") == url)
        {
            if($(this).parent().parent().hasClass('templatemo-submenu'))
            {
                if($(this).parent().parent().parent().hasClass('open'))
                {
                    console.log('skip')
                }
                else
                    $(this).parent().parent().parent().addClass('open')
            }
            console.log('newbee')
            $(this).parent().addClass('active');
        }
    })
}); // document.ready

$(document).ready(function() {
	
	$('#likes').click(function(){
	        var catid;
	        catid = $(this).attr("data-catid");
	         $.get('/rango/like_category/', {category_id: catid}, function(data){
	                   $('#like_count').html(data);
	                   $('#likes').hide();
	               });
    });


    $('#suggestion').keyup(function(){
            var query;
            query = $(this).val();
            $.get('/adm/suggest_category/', {suggestion: query}, function(data){
                     $('#cats').html(data);
            });
	});


    $('#suggestion_rol').keyup(function(){
            var query;
            query = $(this).val();
            $.get('/adm/suggest_rol/', {suggestion: query}, function(data){
                     $('#cats_rol').html(data);
            });
	});

    $('#suggestion_permiso').keyup(function(){
            var query;
            query = $(this).val();
            $.get('/adm/suggest_permiso/', {suggestion: query}, function(data){
                     $('#cats_permiso').html(data);
            });
	});

	$('.rango-add').click(function(){
	    var catid = $(this).attr("data-catid");
        var url = $(this).attr("data-url");
        var title = $(this).attr("data-title");
        var me = $(this)
	    $.get('/rango/auto_add_page/', {category_id: catid, url: url, title: title}, function(data){
	                   $('#pages').html(data);
	                   me.hide();
	               });
    });;
});

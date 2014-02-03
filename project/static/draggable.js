var id = 0;

$(document).ready(function(){
			  
});
		  
function addNewPhoto() {
	$("#newslideitem").submit();
}

var css = "";

function recursiveIterate($node) {
    $node.children().each(function() {
		if ($(this).attr('id') != undefined && !$(this).is('img')) {
			css += '#';
			css += $(this).attr('id');
			css += ': {\n\theight: ';
			css += $(this).height();
			css += ';\n\twidth: ';
			css += $(this).width();
			css += ';\n\tposition: relative;\n\t left: ';
			css += $(this).position().left;
			css += ';\n\t top: ';
			css += $(this).position().top;
			css += ';\n}\n';
		}
		 recursiveIterate($(this));
    });
}

function save(album_id) {
	
	console.log("Save"+album_id);
	recursiveIterate($("#content"));
	css += 'img {\n\twidth: 100%;\n\theight: 100%;\n\t}\n.frame {\n\tmax-width: 640;\n\tmax-height: 640px;\n\twidth: auto;\n\theight: auto;\n}';
	//console.log(css);
	$.ajax({
		type: "POST",
		url:"/albumsave/",
		data: {
		'css': css,
		'album_id': album_id,
		},
		success: function(){
		 },
		error: function(){
			alert("Error");
	}});
}
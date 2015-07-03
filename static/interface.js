//Item's interaction
function newItem(){
	var form = $('#add_item');
	var name = form.find('.name').val();
	var category = form.find('.category').val();
	var description = form.find('.description').val();
	$.ajax({
		type:'POST',
		url:'/item/new?state='+$('#stateHolder').attr('data-state'),
		processData:false,
		contentType: 'application/octet-stream; charset=utf-8',
		data: JSON.stringify({'name':name,'category':category,'description':description}),
		success: function(response){
			console.log('new item created');
			window.location.href="/"
		},
		error: function(response){
			console.log('Error tryng to create a new item.');
			console.log(response);
		}
	});
};
function editItem(elementoDOM){
	var form = $(elementoDOM).closest('.edit');
	var id = form.find('.item_id').html();
	var userId = form.find('.user_id').html();
	var name = form.find('.name').val();
	var category = form.find('.category').val();
	var description = form.find('.description').val();
	$.ajax({
		type:'POST',
		url:'/item/edit?state='+$('#stateHolder').attr('data-state'),
		processData:false,
		contentType: 'application/octet-stream; charset=utf-8',
		data: JSON.stringify({'id':id,'userId':userId,'name':name,'category':category,'description':description}),
		success: function(response){
			console.log('Item edited');
			window.location.href="/"
		},
		error: function(response){
			console.log('Error tryng to edit a item.');
			console.log(response);
		}
	});
};
function checkDelete(elementoDOM){
	var id = $(elementoDOM).attr('data-itemId');
	var userId = $(elementoDOM).attr('data-userId');
	var confirmation = $('#deleteConfirmation');
	confirmation.find('.item_id').text(id);
	confirmation.find('.user_id').text(userId);
	confirmation.fadeIn(300);
}
function deleteItem(elementoDOM){
	var form = $(elementoDOM).closest('.delete_confirmation');
	var id = form.find('.item_id').html();
	var userId = form.find('.user_id').html();
	$.ajax({
		type:'POST',
		url:'/item/delete?state='+$('#stateHolder').attr('data-state'),
		processData:false,
		contentType: 'application/octet-stream; charset=utf-8',
		data: JSON.stringify({'id':id,'userId':userId}),
		success: function(response){
			console.log('Item deleted');
			window.location.href="/"
		},
		error: function(response){
			console.log('Error tryng to delete a item.');
			console.log(response);
		}
	});
};
function cancelDelete(){
	$('#deleteConfirmation').fadeOut(300);
}
function hideBack(elementoDOM){
	$(elementoDOM).closest('.popUp').fadeOut(300);
};
//Screen interaction
function showAddItem(elementoDOM){
	var elemento = $(elementoDOM);
	if(elemento.attr('data-status') == "hide"){//If they are hidden it shows them
		elemento.attr('data-status','show');
		$('#add_item').slideDown(300);
	}else{//If they are visible it hides them
		elemento.attr('data-status','hide');
		$('#add_item').slideUp(300);
	};
}
function hideAddItem(){
	$('#add_item').slideUp(300);
}
function showDescription(elementoDOM){
	var elemento = $(elementoDOM);
	var description = elemento.closest('.item').find('.description')
	if(elemento.attr('data-status') == "hide"){//If they are hidden it shows them
		elemento.attr('data-status','show');
		description.slideDown(300);
	}else{//If they are visible it hides them
		elemento.attr('data-status','hide');
		description.slideUp(300);
	};
}
function showEdit(elementoDOM){
	var elemento = $(elementoDOM);
	var edit = elemento.closest('.item').find('.edit');
	if(elemento.attr('data-status') == "hide"){//If they are hidden it shows them
		elemento.attr('data-status','show');
		edit.slideDown(300);
	}else{//If they are visible it hides them
		elemento.attr('data-status','hide');
		edit.slideUp(300);
	};
}
function hideEdit(elementoDOM){
	var elemento = $(elementoDOM);
	var edit = elemento.closest('.item').find('.edit');
	var editButton = elemento.closest('.item').find('.b_edit');
	edit.slideUp(300);
	editButton.attr('data-status','hide');
};
function showLogin(elementoDOM){
	var elemento = $(elementoDOM);
	if(elemento.attr('data-status') == "hide"){//If they are hidden it shows them
		elemento.attr('data-status','show');
		$('#logIn_area').slideDown(300);
	}else{//If they are visible it hides them
		elemento.attr('data-status','hide');
		$('#logIn_area').slideUp(300);
	};
}
function showHidden(elementoDOM){//Makes the elements of the class hide apear or desapear
	var elemento = $(elementoDOM);
	if(elemento.attr('data-status') == "hide"){//If they are hidden it shows them
		elemento.attr('data-status','show');
		elemento.closest('.unit').find('.hide.'+elemento.attr('data-target')).slideDown(300);
	}else{//If they are visible it hides them
		elemento.attr('data-status','hide');
		elemento.closest('.unit').find('.hide.'+elemento.attr('data-target')).slideUp(300);
	};
};
function closeEdit(elementoDOM){//Close the edit block
	var elemento = $(elementoDOM);
	elemento.closest('.unit').find('.hide.edit_form').slideUp(300);
	elemento.closest('.unit').find('.edit').attr('data-status','hide');
}
function closeDelete(elementoDOM){//Close the delete block
	var elemento = $(elementoDOM);
	elemento.closest('.unit').find('.hide.delete_form').slideUp(300);
	elemento.closest('.unit').find('.delete').attr('data-status','hide');
}
function closeNew(elementoDOM){//Close the delete block
	var elemento = $(elementoDOM);
	elemento.closest('.unit').find('.hide.new_form').slideUp(300);
	elemento.closest('.unit').find('.new').attr('data-status','hide');
}
//Resposiviness
$(window).resize(function(){//roda qdo a janela muda de tamanho
	if ($(window).width() > 510 ){
		var elemento = $('#menu');
		if(elemento.attr('data-status') == "hide"){//If they are hidden it shows them
			elemento.attr('data-status','show');
			elemento.show();
		}
	}else{
		var elemento = $('#menu');
		if(elemento.attr('data-status') == "show"){
			elemento.attr('data-status','hide');
			elemento.hide();
		};
	};
});
function showMenu(){//qdo o meno esta escondido essa funcao faz ele aparecer
	var elemento = $('#menu');
	if(elemento.attr('data-status') == "hide"){//If they are hidden it shows them
		elemento.attr('data-status','show');
		elemento.fadeIn( "slow" );//.slideDown(300);
	}else{//If they are visible it hides them
		elemento.attr('data-status','hide');
		elemento.fadeOut( "slow" );//.slideUp(300);
	};
}
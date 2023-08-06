function in_progres(width,$this,id_crm) {
	
		$($this).css("width",width);
		if(width=="25%")
		{$($this).css("background-color","#dc3545");
		$(".fila."+id_crm).css("background","#ff00004d");}
		else if(width=="50%")
		{$($this).css("background-color","#ff9007");
		$(".fila."+id_crm).css("background","#ffa5004d");}
		else if(width=="75%")
		{$($this).css("background-color","#ffc107");
		$(".fila."+id_crm).css("background","#ffff004d");}
		else if(width=="100%")
		{$($this).css("background-color","#28a745");
		$(".fila."+id_crm).css("background","#0080004d");
		}
		else
		{$(".fila."+id_crm).css("background","#ffffff");}
}
$(document).ready(function(){
	$( ".progress-item" ).each(function() {
		var width=$(this).attr("data-width");
		var id_crm=$(this).attr("id");
		
		in_progres(width,this,id_crm);


	});
	$( "[name*='vendedor']" ).each(function() {
		$(this).addClass("hidden");
		var number=$(this).parent().attr("id");
		$(this).addClass("pedido"+number);
	});
	$("#menu").hide();
    $('#id_inicio').datetimepicker({
        format:'d/m/Y',
        inline:false
    });
    $('#id_fin').datetimepicker({
        format:'d/m/Y',
        inline:false
    });
    $('#id_inicio').attr("autocomplete","off");
	$('#id_fin').attr("autocomplete","off");

	$( "[name*='venta_ven']" ).each(function() {

		var vendedor=$(this).text();
		
		var id=$(this).attr("id");

		if(vendedor == 'None')
		{
			$('#ven'+id+'.vendedor_asignado').addClass("hidden");
			$('#vensin'+id+'.vendedor_sinasignar').removeClass("hidden");
		}
		else
		{
			$('#ven'+id+'.vendedor_asignado').removeClass("hidden");
			$('#vensin'+id+'.vendedor_sinasignar').addClass("hidden");
		}
	});	
});
$('#id_llamada').change(function() {
	$('.form').submit();
});
$( ".send_correo" ).click(function() {
	$(".banner_carga").removeClass("hidden");
	$(".all_").addClass("hidden");
	var id_crm=$(this).attr("id");

		$.ajax({
		url: '/pedidos/enviar_correo/',
		type: 'get',
		data: {
		'id': id_crm,
		},
		success: function (data) {
			alert(data.mensaje)
			$(".banner_carga").addClass("hidden");
			$(".all_").removeClass("hidden");

			}
		});
});

$( ".asignar" ).click(function() {

  var number=$(this).attr("id");
  $(this).addClass("hidden");
  
  $(".pedido"+number).removeClass("hidden");
  $(".btncancel"+number).removeClass("hidden");
  $(".vendedor_asign").addClass("hidden");

 
});
$( ".cancelar" ).click(function() {

  var number=$(this).attr("id");
  $(this).addClass("hidden");
  $(".pedido"+number).addClass("hidden");
  $(".asign"+number).removeClass("hidden");
  $(".btn"+number).addClass("hidden");
  $(".vendedor_asign"+number).removeClass("hidden");
 
});
$( ".guardar" ).click(function() {
	var id_crm=$(this).attr("id");
	var id_cliente=$(".pedido"+id_crm).val();

	
	
 	if(id_crm && id_vendedor)
	{
		$.ajax({
		url: '/pedidos/vendedor_asignar/',
		type: 'get',
		data: {
			'id_vendedor': id_cliente,
			'id_crm':id_crm,
		},
		success: function (data) {
				if(data.mensaje!="")
				{
					$('.cancelar').trigger("click");
					$('span.vendedor_asign'+id_crm).text(data.mensaje);
					$('#ven'+id_crm+'.vendedor_asignado').removeClass("hidden");
					$('#vensin'+id_crm+'.vendedor_sinasignar').addClass("hidden");
				}
				else
				{alert(data.mensaje)}				
			}
		});
	}
 
});
function progreso_(id_crm,progreso)
{	$(".fin_state").addClass("hidden");
		
		if(progreso=="0")
	{
		$("#change_state"+id_crm+" .return_state").addClass("hidden");
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#dc3545");
		$("#change_state"+id_crm+" .change_state").html('Inicio <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$(".fin_state").removeClass("hidden");
		$("#change_state"+id_crm+" .fin_state").css("background-color","#28a745");
		$("#change_state"+id_crm+" .fin_state").html('Entregado <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
	}	
	else if(progreso=="25")
	{
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .return_state").removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#ff9007");
		$("#change_state"+id_crm+" .change_state").html('Finalizado <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$("#change_state"+id_crm+" .return_state").css("background-color","#ccc");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Recibido');
	}
	else if(progreso=="50")
	{
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .return_state").removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#ffc107");
		$("#change_state"+id_crm+" .change_state").html('Aviso a cliente <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$("#change_state"+id_crm+" .return_state").css("background-color","#dc3545");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Inicio');
	}
	else if(progreso=="75")
	{
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .return_state").removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#28a745");
		$("#change_state"+id_crm+" .change_state").html('Entregado <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$("#change_state"+id_crm+" .return_state").css("background-color","#ff9007");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Finalizado');
	}
	else{
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .return_state").removeClass("hidden");
		$(".fin_state").addClass("hidden");
		$("#change_state"+id_crm+" .return_state").css("background-color","#ffc107");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Aviso a cliente');
	}
}
$( ".progress" ).on("touchstart",function(){
	var id_crm=$(this).attr("id");
	var progreso=$(this).attr("data-value");

	progreso_(id_crm,progreso);
});

$( ".progress" ).dblclick(function() {
	var id_crm=$(this).attr("id");
	var progreso=$(this).attr("data-value");

	progreso_(id_crm,progreso);


	//alert(id_crm)

});
$( ".fin_state" ).click(function() {
	var id_crm=$(this).attr("id");
	 if(id_crm)
	{
		$.ajax({
		url: '/pedidos/fin_progress/',
		type: 'get',
		data: {
			'id_crm':id_crm,
		},
		success: function (data) {
			if(data != "")
			{
				in_progres(data+"%","span#"+id_crm+".progress-item",id_crm);
				$("span#"+id_crm+".progress-item").text(data+"%");
				progreso_(id_crm,data);
			}
			else
			{alert(data.mensaje)}	
		}
		});
	}
});
$( ".change_state" ).click(function() {
	var id_crm=$(this).attr("id");
	 if(id_crm)
	{
		$.ajax({
		url: '/pedidos/change_progress/',
		type: 'get',
		data: {
			'id_crm':id_crm,
		},
		success: function (data) {
			if(data != "")
			{
				in_progres(data+"%","span#"+id_crm+".progress-item",id_crm);
				$("span#"+id_crm+".progress-item").text(data+"%");
				progreso_(id_crm,data);
			}
			else
			{alert(data.mensaje)}	
		}
		});
	}
});
$( ".return_state" ).click(function() {
	var id_crm=$(this).attr("id");
	 if(id_crm)
	{
		$.ajax({
		url: '/pedidos/return_progress/',
		type: 'get',
		data: {
			'id_crm':id_crm,
		},
		success: function (data) {
			if(data != "")
			{
				in_progres(data+"%","span#"+id_crm+".progress-item",id_crm);
				$("span#"+id_crm+".progress-item").text(data+"%");
				
				progreso_(id_crm,data);
			}
			else
			{alert(data.mensaje)}	
		}
		});
	}
});
$("[name*='vendedor']").on("change",function(){
	var valor=$(this).val();
	var number=$(this).parent().attr("id");
	if(valor != '')
	{	
		$(".btn"+number).removeClass("hidden");
	}
	else
	{$(".btn"+number).addClass("hidden");}
});
$( ".more" ).click(function() {
	var id_doc=$(this).attr("id");
	if($(this).hasClass("glyphicon-triangle-right"))
	{
		$(this).removeClass("glyphicon-triangle-right");
		$(this).addClass("glyphicon-triangle-bottom");
		$(".det"+id_doc).removeClass("hidden");
		$('.det'+id_doc+' #contenido').empty();


		$.ajax({
		url: '/pedidos/get_detalles/',
		type: 'get',
		data: {
			'id_doc': id_doc,
		},
		success: function (data) {
				
				for (var i = 0; i <= data.length-1; i++) {
					var html='<div class="col-lg-12 col-md-12 col-xs-12 col-sm-12"><div class="col-lg-4 col-md-4 col-xs-4 col-sm-4">'+data[i].unidades+'</div><div class="col-lg-4 col-md-4 col-xs-4 col-sm-4">'+data[i].articulo +'</div><div class="col-lg-4 col-md-4 col-xs-4 col-sm-4">'+data[i].notas+'</div></div>'
					$('.det'+id_doc+' #contenido').append(html);
				}
			}
		});
	}
	else
	{
		$(this).addClass("glyphicon-triangle-right");
		$(this).removeClass("glyphicon-triangle-bottom");
		$(".det"+id_doc).addClass("hidden");
	}
});
$( ".det_progreso" ).click(function() {
	var id_crm=$(this).attr("id");
	$("#tiempo_espera").html('');
	$("#tiempo_fin").html('');
	$("#tiempo_aviso").html('');
	$("#tiempo_entrega").html('');
	if (id_crm)
	{
		$.ajax({
		url: '/pedidos/get_tiempos/',
		type: 'get',
		data: {
			'id_crm': id_crm,
		},
		success: function (data) {

					if(data)
					{	
						if(data.tiempo_espera)
						{$("#tiempo_espera").html(data.tiempo_espera);}
						if(data.tiempo_fin)
						{$("#tiempo_fin").html(data.tiempo_fin);}
						if(data.tiempo_aviso)
						{$("#tiempo_aviso").html(data.tiempo_aviso);}
						if(data.tiempo_entrega)	
						{$("#tiempo_entrega").html(data.tiempo_entrega);}
					}
			}
		});
	}

});
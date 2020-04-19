function informacionTablas(nombre){
   $(nombre).DataTable(

   {
        "language": {
         "decimal":        "",
    "emptyTable":     "Sin Articulos",
    "info":           "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
    "infoEmpty":      "Mostrando 0 a 0 de 0 Entradas",
    "infoFiltered":   "(filtrado de _MAX_ entradas totales)",
    "infoPostFix":    "",
    "thousands":      ",",
    "lengthMenu":     "Mostrar _MENU_ entradas",
    "loadingRecords": "Cargando...",
    "processing":     "Procesando...",
    "search":         "Buscar:",
    "zeroRecords":    "No matching records found",
    "paginate": {
        "first":      "Primero",
        "last":       "Anterior",
        "next":       "Siguiente",
        "previous":   "Previo"
    },
    "aria": {
        "sortAscending":  ": activate to sort column ascending",
        "sortDescending": ": activate to sort column descending"
    }



        }
    }

    );

}




  function cargarPagina(){
    location.reload();
    }


function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
 }

function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



function configurarCSRF(){
var name = 'csrftoken';
var csrftoken =getCookie(name);

$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!  csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

}//final de petSe


function cargarPagina(){
    location.reload();
}

function Peticiones(url,metodo,tipo,mms){



 $.ajax({
        url : url,
        type: metodo,
        data : tipo,

    }).done(function(msg){ //

        var objeto = JSON.parse(JSON.stringify(msg));

        if(objeto.message == "Cambio realizado con exitoso"){
        // console.debug(objeto.message);
        $(mms).html(objeto.message);
        setTimeout(cargarPagina,2000);
        }else{
         //console.debug(objeto.message);
        $(mms).html(objeto.message);
        $('.submitBtn').removeAttr("disabled");
        }


    });


}


  function eventoTecla(input,numMetodo){

    var input = document.getElementById(input)
    input.addEventListener("keyup", function(event) {
      if (event.keyCode === 13) {
        event.preventDefault();
        callMet(numMetodo);

      }
    });
     }


    function callMet(id){
    switch (id) {

        case 1:
        submitContactForm();
        break;

        case 2:
        submitContactForm2();
        break;

        case 3:
        submitContactForm3();
        break;

        case 4:
        submitContactForm4();
        break;

        default:
        debug.log("Lo sentimos");

        }

    }

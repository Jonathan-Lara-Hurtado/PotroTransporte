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
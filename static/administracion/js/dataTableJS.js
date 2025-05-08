function table(tabla){

   
    
      $('#'+ tabla).DataTable({
  
            //pageLength: 5,
            // "language": {
            //   "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
            // }
            "ordering": false,
            "language": {
             
              "emptyTable": "No hay información",
              "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
              "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
              "infoFiltered": "(Filtrado de _MAX_ total entradas)",
              "lengthMenu": "Mostrar _MENU_ Entradas",
              "loadingRecords": "Cargando...",
              "processing": "Procesando...",
              "search": "Buscar:",
              "zeroRecords": "Sin resultados encontrados",
              "paginate": {
                  "first": "Primero",
                  "last": "Ultimo",
                  "next": "Siguiente",
                  "previous": "Anterior"
              }
            },
            responsive: "true",
            dom: 'Bfrtip',
            buttons:[
              {
                extend: 'excelHtml5',
                text: '<i class="bi bi-file-earmark-spreadsheet"></i>',
                titleAttr: 'Exportar a Excel',
                className: 'btn btn-success btn-sm',
                exportOptions: {
              
                  columns: 'th:not(:last-child)'
              }
              },
              {
                extend: 'pdfHtml5',
                text: '<i class="bi bi-file-earmark-pdf"></i>',
                titleAttr: 'Exportar a PDF',
                className: 'btn btn-danger btn-sm',
                messageTop: 'Reporte emitido:',
              exportOptions: {
              
                columns: 'th:not(:last-child)'
            }
  
              },
              {
                extend: 'print',
                text: '<i class="bi bi-printer"></i>',
                titleAttr: 'Exportar a Imprimir',
                className: 'btn btn-primary btn-sm',
                exportOptions: {
              
                  columns: 'th:not(:last-child)'
              }
    
              }
            ]
          });
    }
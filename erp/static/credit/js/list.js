$(function() {
  $('#data').DataTable({
    responsive: true,
    autoWidth: false,
    destroy: true,
    deferRender: true,
    ajax: {
      url: window.location.pathname,
      type: 'POST',
      data: {
        'action': 'searchdata'
      },
      headers: {
        'X-CSRFToken': csrftoken
      },
      dataSrc: ""
    },
    columns: [
      { "data": "id" },
      { "data": "names" },  // Cliente
      { "data": "lastnames" },  // Cliente
      { "data": "date_joined" },  // Fecha del crédito
      { "data": "status" },  // Estado del crédito
      { "data": "total_credit", "render": $.fn.dataTable.render.number(',', '.', 2, '$') },  // Total
      { "data": "total_paid", "render": $.fn.dataTable.render.number(',', '.', 2, '$') },  // Total
      { "data": "pending_balance", "render": $.fn.dataTable.render.number(',', '.', 2, '$') },  // Abonado
      { "data": "id" },  // Acciones
    ],
    columnDefs: [
      {
        targets: [-1], // Última columna (acciones)
        class: 'text-center',
        orderable: false,
        render: function(data, type, row) {
          var buttons = '<a href="/erp/credit/payment/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-dollar-sign"></i> Pagar</a> ';
          buttons += '<a href="/erp/credit/detail/' + row.id + '/" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i> Ver</a>';
          return buttons;
        }
      },
    ],
  });
});


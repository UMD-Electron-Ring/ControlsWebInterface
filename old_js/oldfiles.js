function successFunction(data) {
  var allRows = data.split(/\r?\n|\r/);
  var table = '<div class="table">';
  for (var singleRow = 0; singleRow < allRows.length; singleRow++) {
    if (singleRow === 0) {
      table += '<div class="row header">';
    } else {
      table += '<div class="row">';
    }
    var rowCells = allRows[singleRow].split(',');
    for (var rowCell = 0; rowCell < rowCells.length; rowCell++) {
    	table += '<div class="cell">';
    	table += rowCells[rowCell];
    	table += '</div>';
    }
	table += '</div>';
  } 
  table += '</div>'; // table
  
  $('body').append(table);
}
function refreshTableCSV() {
    $.ajax({
        type: "GET",
        //url: "https://s3.amazonaws.com/magnetdata/data.csv",
        url: "http://127.0.0.1:5000/csv/",
        success: function (data) {
           successFunction(data);
        }
    });
}
refreshTablePHP();
    $(document).ready(function(){
      refreshTablePHP();
    });

    function refreshTablePHP(){
        $('#tableMain').load('http://127.0.0.1:5000/php/', function(){
           setTimeout(refreshTablePHP, 5000);
        });
    }
	//refreshTable(); // on page loading
	//setInterval(function(){refreshTable()}, 5000);
</script>

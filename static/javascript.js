//https://stackoverflow.com/questions/18796221/creating-a-select-box-with-a-search-option
$(document).ready(function () {
   $('select').selectize({
         sortField: 'text',
 });
  });

//https://stackoverflow.com/questions/5024056/how-to-pass-parameters-on-onchange-of-html-select
function getCurrency(selectObject) {
  var value = selectObject.value.split('----')[1];  
  var valuePrice = document.querySelector('#select-currency-delete').getAttribute(value);
  document.querySelector('.delete-price').setAttribute('value', value);
  console.log(value);
}



//value = $( "#select-currency_delete" ).val();
//console.log(value);







var searchfield = document.getElementById('searchfield');
var searchform = document.getElementById("searchform");
    searchform .addEventListener("submit", function (e) {
        e.preventDefault();
        if(searchfield.value != '') {
            location.href = `/search_result?query=${searchfield.value}`;
        }
        
  });
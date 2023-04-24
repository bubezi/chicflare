let el = document.getElementById('form1');


$(document).ready(function() {
    $("#form1").toggle();
    $("#formButton").click(function() {
      $("#form1").toggle();
      el.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});
    });
  });


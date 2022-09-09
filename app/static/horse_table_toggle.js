$(document).ready(function() {
    $("#horse_data_table").DataTable({
      paging: false
    }
    );

    $(".detailed_gp").hide();
    $(".discipline_gp").hide();
    $(".confo_total").hide();
    $(".confo").hide();

    function toggleAttrsFromBtn(btn_selector, toggle_selector, btn_subject) {
      $(toggle_selector).toggle();    
      if($(btn_selector).val() == "Hide " + btn_subject) {
        $(btn_selector).val("Show " + btn_subject);
      } else {
        $(btn_selector).val("Hide " + btn_subject);
      }
    }

    $("#btn_show_gp").click(function() {
      toggleAttrsFromBtn("#btn_show_gp", ".detailed_gp", "Detailed GP");
    });

    $("#btn_show_discipline_gp").click(function() {
      toggleAttrsFromBtn("#btn_show_discipline_gp", ".discipline_gp", "Discipline GP");
    });

    $("#btn_show_confo").click(function() {
      toggleAttrsFromBtn("#btn_show_confo", ".confo", "Confo");
    });

    $("#btn_show_confo_totals").click(function() {
      toggleAttrsFromBtn("#btn_show_confo_totals", ".confo_total", "Confo Totals");
    });
  });
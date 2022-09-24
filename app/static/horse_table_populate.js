function populateTable(userID, username) {
  $.getJSON({url: "/api/horse-table/"+userID, timeout: 0}, (data) => {
    console.log(data);
    
    // set heading
    $("#username").text(username + "'s Horses").attr("id", "top");

    // thead
    topRow(data);

    // tbody
    data.forEach(horse => {
      const row = $("<tr></tr>");
      const tdString = "<td></td>"

      const externalLink = "https://www.horsereality.com/horses/" + horse.lifenumber + "/" + horse.name;
      linkObj = $("<a>" + horse.name + "</a>").attr("href", externalLink).attr("target", "_blank");
      $(tdString).append(linkObj).addClass("default-caps").appendTo(row);
      
      $(tdString).text(horse.lifenumber).appendTo(row);
      $(tdString).text(horse.breed.replaceAll("_", " ")).appendTo(row);
      $(tdString).text(horse.sex).appendTo(row);

      $(tdString).text(horse.foal == true ? "Yes" : "No").appendTo(row);
      $(tdString).text(horse.total_gp).appendTo(row);

      addStatsToRow(horse, row, "gp_stats", "detailed-gp");
      addStatsToRow(horse, row, "discipline_gp", "discipline-gp");
      addStatsToRow(horse, row, "confo_stats", "confo");
      addStatsToRow(horse, row, "confo_totals", "confo-totals");

      $("tbody").append(row);
    });

    // apply jquery datatables
    $("#horse-data-table").addClass("display table table-striped table-hover");
    $("#horse-data-table").DataTable({
      paging: false
    });
    
    // hide detailed table columns
    $(".detailed-gp").hide();
    $(".discipline-gp").hide();
    $(".confo-totals").hide();
    $(".confo").hide();

    // make detailed columns toggleable  
    $("#btn-show-gp").click(function() {
      toggleAttrsFromBtn("#btn-show-gp", ".detailed-gp", "Detailed GP");
    });
  
    $("#btn-show-discipline-gp").click(function() {
      toggleAttrsFromBtn("#btn-show-discipline-gp", ".discipline-gp", "Discipline GP");
    });
  
    $("#btn-show-confo").click(function() {
      toggleAttrsFromBtn("#btn-show-confo", ".confo", "Confo");
    });
  
    $("#btn-show-confo-totals").click(function() {
      toggleAttrsFromBtn("#btn-show-confo-totals", ".confo-totals", "Confo Totals");
    });

    //reveal completed table
    $("#loading").hide();
    $("#full-table").show();;
      
  })
  .fail(function(jqXHR, textStatus, errorThrown) {
    console.log("error " + textStatus);
    console.log("incoming Text " + jqXHR.responseText);
  });
}

function topRow(data) {
  addKeysToTopRow(data, "gp_stats", "detailed-gp");
  addKeysToTopRow(data, "discipline_gp", "discipline-gp");
  addKeysToTopRow(data, "confo_stats", "confo");
  addKeysToTopRow(data, "confo_totals", "confo-totals")
}

function addKeysToTopRow(data, dict, className) {
  Object.keys(data[0][dict]).forEach(k => {
    $("<th>" + k.replaceAll("_", " ") + "</th>").addClass(className).appendTo("#top-row");
  });
}

function addStatsToRow(horse, row, key, className) {
  Object.values(horse[key]).forEach(v => {
    if (typeof v == "string") v = v.replaceAll("_", " ");
    $("<td>" + v + "</td>").addClass(className).appendTo(row);
  });
}

function toggleAttrsFromBtn(btnSelector, toggleSelector, btnText) {
  $(toggleSelector).toggle();    
  if($(btnSelector).val() == "Hide " + btnText) {
    $(btnSelector).val("Show " + btnText);
  } else {
    $(btnSelector).val("Hide " + btnText);
  }
}
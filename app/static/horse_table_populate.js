function populateTable(userID, username) {
  $.getJSON({url: "/api/horse-table/"+userID, timeout: 0}, (data) => {
    console.log(data);
    
    // set heading
    $("#username").text(username + "'s Horses").attr("id", "top");

    let icelandicHorseIndex = -1;

    // tbody
    const tbody = $("tbody");
    const tdString = "<td></td>"

    data.forEach((horse, index) => {
      if (horse.breed == "icelandic_horse") icelandicHorseIndex = index;

      const row = $("<tr></tr>");

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

      tbody.append(row);
    });

    // thead
    topRow(data, icelandicHorseIndex);

    // add extra td cells for non icelandic horses if one was present
    if (icelandicHorseIndex >= 0) {
      tbody.children().each((i, element) => {
        if ($(element).children().filter(":nth-child(3)").text() != "icelandic horse") {
          for (let i=0; i<2; i++) $(element).children().filter(":nth-child(27)").after($(tdString).addClass("confo"));
        } 
      });
    }

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

    $("#loading").hide();
    
  });
}

function topRow(data, icelandicHorseIndex) {
  addKeysToTopRow(data, "gp_stats", "detailed-gp", icelandicHorseIndex);
  addKeysToTopRow(data, "discipline_gp", "discipline-gp", icelandicHorseIndex);
  addKeysToTopRow(data, "confo_stats", "confo", icelandicHorseIndex);
  addKeysToTopRow(data, "confo_totals", "confo-totals", icelandicHorseIndex)
}

function addKeysToTopRow(data, dict, className, icelandicHorseIndex) {
  let i = icelandicHorseIndex == -1 ? 0 : icelandicHorseIndex;
  Object.keys(data[i][dict]).forEach(k => {
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
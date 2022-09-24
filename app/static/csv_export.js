/*
Credit to this StackOverflow thread for the fundamental idea behind this script: 
https://stackoverflow.com/questions/68392446/download-html-table-when-clicked-on-button
*/

function exportTableToCSV(filename) {
    alert("Downloading " + filename);
    var csv = [];
    csv.push(['Name','#','Breed','Sex','Foal?','Total GP','Acceleration','Agility',
        'Balance','Bascule','Pulling Power','Speed','Sprint','Stamina','Strength','Surefootedness',
        'Dressage GP','Driving GP','Endurance GP','Eventing GP','Flat Racing GP','Show Jumping GP',
        'Western Reining GP','Walk','Trot','Canter','Gallop','Posture','Head','Neck','Back','Shoulders',
        'Frontlegs','Hindquarters','Socks','Confo Very Good','Confo Good','Confo Average','Confo Below Average',
        'Confo Poor'])

    var rows = document.querySelectorAll("table tr");
  
    for (var i = 1; i < rows.length; i++) {
        var row = [];
        var cols = rows[i].querySelectorAll("td, th");
  
        for (var j = 0; j < cols.length; j++) row.push(cols[j].innerText);
  
        csv.push(row.join(","));
    }
    csv = csv.join("\n")

    csvFile = new Blob([csv], {
        type: "text/csv"
    });
    
    downloadLink = document.createElement("a");
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    
    // Hide download link
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    
    downloadLink.click();
  
  }
  
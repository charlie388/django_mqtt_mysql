document.getElementById("myForm").addEventListener("submit", async (e) => {
    e.preventDefault(); // stop normal form submit

    // Collect values from inputs
    const topic = document.getElementById("topic").value;
    const msg = document.getElementById("msg").value;

    // Build JSON object
    const payload = {
      topic: topic,
      msg: msg
    };

    try {
      const response = await fetch("/api/publish/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();
      console.log("Server response:", result);
    } catch (error) {
      console.error("Error:", error);
    }
});

let idMark = null;
setInterval(add, 5000);
  function add() {
    if(idMark == null) { // fresh get
      getUpload('/api/upload/');	
    } else {
      getUpload('/api/upload/'+idMark);	
    }
    
  }
  
  function getUpload(URL)
  {
    fetch(URL) // Replace with your API endpoint
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON data
      })
      .then(data => {
        //console.log(data); // Handle the data here
        fillTable(data);

      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
  }
  
let toggleColor = 0;
  function fillTable(data) {
    var table = document.getElementById("myTable").getElementsByTagName('tbody')[0];
    for(let i=(data.length-1); i>=0; i--) {
      var newRow = table.insertRow(0);

      toggleColor = toggleColor % 6;
      if(toggleColor == 0) {
        newRow.classList.add("table-primary");
        toggleColor++;
      } else if(toggleColor == 1){
        newRow.classList.add("table-success");
        toggleColor++;
      } else if(toggleColor == 2){
        newRow.classList.add("table-danger");
        toggleColor++;
      } else if(toggleColor == 3){
        newRow.classList.add("table-warning");
        toggleColor++;
      } else if(toggleColor == 4){
        newRow.classList.add("table-info");
        toggleColor++;
      } else if(toggleColor == 5){
        newRow.classList.add("table-light");
        toggleColor++;
      }

      var idCell = newRow.insertCell(0);
      var deviceCell = newRow.insertCell(1);
      var uploadCell = newRow.insertCell(2);
      var eventTimeCell = newRow.insertCell(3);
      
      idCell.innerHTML = data[i].id;
      deviceCell.innerHTML = data[i].device;
      uploadCell.innerHTML = data[i].upload;
      //eventTimeCell.innerHTML = new Date(data[i].created);
      eventTimeCell.innerHTML = new Date(data[i].created).toLocaleString();

      idMark = data[i].id;
    }
    
      if(table.rows.length > 13) {
          let i;
          for(i=table.rows.length - 1 ; i>=13; i--) {
            table.deleteRow(i);
          }
      }
  }

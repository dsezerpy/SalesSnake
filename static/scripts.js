
function setDate(target){
  target.valueAsDate=new Date();
  target.max=target.value;
}


function toggle_add_form(){
  let element = document.getElementById("addStock");
  if (element.style.display === "none") {
    element.style.display = "flex";
    setDate(document.getElementById('date'))
  } else {
    element.style.display = "none";
  }
}

function toggle_detail(name){
  let element = document.getElementById("detailform");
  if (element.style.display === "none") {
    get_history(name)
    element.style.display = "flex";
  } else {
    element.style.display = "none";
  }
}

function toggle_edit(name){
  let element = document.getElementById("detailform");
  if (element.style.display === "none") {
    element.style.display = "flex";
  } else {
    element.style.display = "none";
  }
}function toggle_sale(name){
  let element = document.getElementById("detailform");
  if (element.style.display === "none") {
    element.style.display = "flex";
  } else {
    element.style.display = "none";
  }
}

function get_history(name){
  let url=document.documentURI + "/detail/"+name
  fetch(url,{mode: 'no-cors'}).then((resp)=>{
    resp.json().then((obj)=>{
      var table = document.createElement("table")
      var tbody=document.createElement("tbody")
      var header=document.createElement("tr")
      header.className="item header";
      ["Date","Price", "Item Amount"].forEach(function(item){
        var cell = document.createElement('td');
        cell.appendChild(document.createTextNode(item))
        header.appendChild(cell)
      })
      tbody.appendChild(header)
      obj.forEach(function(item){
        console.log(item)
        var row=document.createElement("tr")
        row.className="item";
        [Date(obj['date']),obj['price'],obj['amount']].forEach(function (item) {
          console.log(item.toString())
          var cell = document.createElement('td');
          cell.appendChild(document.createTextNode(item))
          row.appendChild(cell)
        })
        table.appendChild(row)
      })
      document.getElementById("itemhistory").appendChild(table)
      /*      <tr class="item">
                    <td>Placeholder</td>
                    <td>Placeholder</td>
                    <td>Placeholder</td>
                </tr>
      */
    })
  })
}
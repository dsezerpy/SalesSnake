function openForm() {
  document.getElementById("addStock").style.display = "flex";
}

function closeForm() {
  document.getElementById("addStock").style.display = "none";
}

function openEditForm() {
  document.getElementById("editStock").style.display = "flex";
}

function closeEditForm() {
  document.getElementById("editStock").style.display = "none";
}

function setDate(target){
  target.valueAsDate=new Date();
  target.max=target.value;
}
setDate(document.getElementById("date"))
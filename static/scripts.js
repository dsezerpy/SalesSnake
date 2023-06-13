
function setDate(target){
  target.valueAsDate=new Date();
  target.max=target.value;
}
setDate(document.getElementById("date"))
function showtoast() {
var toast = document.getElementById("toast");
if (toast.innerHTML == ""){
    console.log("no toast")
    return

}
toast.className = "show";
  
    
setTimeout(()=>{ toast.className = toast.className.replace("show", ""); }, 5000);
}
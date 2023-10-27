var username = document.getElementById("uid");
var password = document.getElementById("pwd");

var login = document.getElementById("login");
var signup = document.getElementById("signup");
login.addEventListener("click", ()=>{
    if (username.value && password.value){
        fetch("/login/auth",{
            method: "POST",
            body: JSON.stringify({
                username: username.value,
                password: password.value,
              }),
              headers: {
                "Content-type": "application/json; charset=UTF-8"
              }
        }).then((response) => response.json).then((json) => console.log(json));
    }
});

signup.addEventListener("click", ()=>{
  if (username.value && password.value){
      fetch("/login/signup",{
          method: "POST",
          body: JSON.stringify({
              username: username.value,
              password: password.value,
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8"
            }
      }).then((response) => response.json).then((json) => console.log(json));
  }
});
    


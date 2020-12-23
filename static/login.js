//ログインボタンのクリック時にIDとパスワードのPOST送信
document.getElementById("login").addEventListener("click", (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault()
  
    const obj = {
       "user_id": document.getElementById("user-id").value,
       "password": document.getElementById("password").value
      };
    console.log(obj)
    const method = "post";
    const body = JSON.stringify(obj);
    console.log(body)
    const headers = {
      'Accept': 'text/html',
      'Content-Type': 'application/json'
    };
  fetch("./user/login", {method, headers, body})
        .then((res)=> res.json())
        .then((res)=> {
          const d1 = document.getElementById("error-alert");
          if (res["message"] == "Error"){
            d1.style.display = "block";
          }
        })
        .catch(console.error);
});
//ログインボタンのクリック時にIDとパスワードのPOST送信
document.getElementById("login").addEventListener("click", (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault()
  
    const obj = { "id": "hogehoge", "password": "PASSWORD"};
    const method = "post";
    const body = JSON.stringify(obj);
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };
  fetch("./haiku/user/login", {method, headers, body}).then((res)=> res.json()).then(console.log).catch(console.error);
  })
  
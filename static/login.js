//ログインボタンのクリック時にIDとパスワードのPOST送信
document.getElementById("login").addEventListener("click", (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault()

    const obj = {
        "user_id": document.getElementById("user-id").value,
        "password": document.getElementById("password").value
    };
    const method = "post";
    const body = JSON.stringify(obj);
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    fetch("./user/login", { method, headers, body })
        .then((res) => res.json())
        .then((res) => {
            const d1 = document.getElementById("error-alert");
            if (res["message"] == "Error") {
                d1.style.display = "block";
            }
            if (res["message"] == "Success") {
                window.location.href = './';
            }
        })
        .catch(console.error);
});
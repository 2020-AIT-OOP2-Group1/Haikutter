
document.getElementById("send").addEventListener('click', (e) => {
  // ボタンイベントのキャンセル
  e.preventDefault()
  const obj = {text: document.getElementById("text").value, name: document.getElementById("name").value};
  const method = "post";
  const body = JSON.stringify(obj);
  const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  };
fetch("./haiku", {method, headers, body}).then((res)=> res.json()).then(console.log).catch(console.error);
});


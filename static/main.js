
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


// メモ : add => fav/ add-submit => favorite / fn => favorite
document.getElementById("favorite").addEventListener("click", (e) => {
  // ボタンイベントのキャンセル
  e.preventDefault()

  const obj = { "id": "fs7UBJYcxOCSN5oSa6zI6MwxUoOknyAB", "date": "2020-12-15-11:11:04", "text": "aaaaaaaaaaaa\n", "name": "aaaaaaa", "favorite": 0 };
  const method = "post";
  const body = JSON.stringify(obj);
  const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  };
fetch("./haiku/favorite", {method, headers, body}).then((res)=> res.json()).then(console.log).catch(console.error);
})

display();

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
    fetch("./haiku", {method, headers, body}).then((res)=> res.json()).then(()=>{display();}).catch(console.error);
});

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
    fetch("./haiku/favorite", {method, headers, body}).then((res)=> res.json()).then(()=>{display();}).catch(console.error);
})

function display(){
    fetch("./haiku")
    .then((res)=> res.json())
    .then((res)=>{
        document.getElementById("haiku-body").innerHTML = "";
        res.forEach((val)=>{
            const haikuCard = 
            `
                <div class="card shadow-sm mb-3">
                    <div class="card-body">
                        <p class="fs-2 lh-1 text-center">${val['text']}</p>
                        <p class="fs-5 lh-1 text-end">${val['name']}</p>
                        <p class="fs-7 lh-1 text-muted text-end">${val['date']}</p>
                    </div>
                </div>
            `

            document.getElementById("haiku-body").innerHTML += haikuCard;
        })
    })
    .catch(console.error);
}
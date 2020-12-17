display();

document.getElementById("send").addEventListener('click', (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault();
    const obj = {text: document.getElementById("text").value, name: document.getElementById("name").value};
    const method = "post";
    const body = JSON.stringify(obj);
    const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    };
    fetch("./haiku", {method, headers, body}).then((res)=> res.json()).then(()=>{display();}).catch(console.error);
});

function favorite(val){
    const obj = { "id": val};
    const method = "post";
    const body = JSON.stringify(obj);
    const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    };
    fetch("./haiku/favorite", {method, headers, body}).then((res)=> res.json()).then(()=>{display();}).catch(console.error);
}

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
                        <p class="fs-2 lh-1 text-center mt-3">${val['text']}</p>
                        <div class="text-end">
                            <div class="row align-items-center d-flex justify-content-between">
                                <div class="col-auto align-self-end">
                                    <button type="button" class="btn btn-secondary mb-3 favorite" onclick="favorite('${val['id']}')">
                                        <i class="far fa-heart"> ${val['favorite']}</i>
                                    </button>
                                </div>
                                <div class="col-auto"> 
                                    <p class="fs-5 lh-1">${val['name']}</p>
                                    <p class="fs-7 lh-1 text-muted">${val['date']}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `

            document.getElementById("haiku-body").innerHTML += haikuCard;
        })
    })
    .catch(console.error);
}
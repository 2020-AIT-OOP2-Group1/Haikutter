display();

document.getElementById("send").addEventListener('click', (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault();
    const obj = { text: document.getElementById("text").value };
    const method = "post";
    const body = JSON.stringify(obj);
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    fetch("./haiku", { method, headers, body })
        .then((res) => res.json())
        .then((res) => {
            display();
            const d1 = document.getElementById("error-alert");
            if (res["message"] == "Error") {
                d1.style.display = "block";

            } if (res["message"] == "Success") {
                display();
            }
        }).catch(console.error);
});

//logout
document.getElementById("logout").addEventListener("click", (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault()

    const obj = {};
    console.log(obj)
    const method = "post";
    const body = JSON.stringify(obj);
    console.log(body)
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    fetch("./user/logout", { method, headers, body })
        .then((res) => res.json())
        .then((res) => {
            const d1 = document.getElementById("error-alert");
            if (res["message"] == "Error") {
                d1.style.display = "block";
            }
            if (res["message"] == "Success") {
                window.location.href = './login';
            }
        })
        .catch(console.error);
});

function favorite(val) {
    const obj = { "id": val };
    const method = "post";
    const body = JSON.stringify(obj);
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    fetch("./haiku/favorite", { method, headers, body }).then((res) => res.json()).then(() => { display(); }).catch(console.error);
}

function display() {
    fetch("./haiku")
        .then((res) => res.json())
        .then((res) => {
            document.getElementById("haiku-body").innerHTML = "";
            res.forEach((val) => {
                const haikuCard =
                    `
                <div class="card shadow-sm mb-3">
                    <div class="card-body">
                        <p class="fs-2 lh-1 text-center mt-3" style="font-family: 'Noto Serif JP', serif;">${val['text']}</p>
                        <div class="text-end">
                            <div class="row align-items-center d-flex justify-content-between">
                                <div class="col-auto align-self-end">
                                    <button type="button" class="btn ${(val['liked'] == "True") ? "btn btn-primary" : "btn-secondary"} mb-3 favorite" onclick="favorite('${val['id']}')">
                                        <i class="${(val['liked'] == "True") ? "fas" : "far"} fa-heart"> ${val['favorite']}</i>
                                    </button>
                                </div>
                                <div class="col-auto">
                                    <img src="/${val['user']['image']}" style="object-fit: cover; width: 2rem; height: 2rem;" class="border rounded-circle mb-1">
                                    <a href="./user/${val['user']['id']}" class="link-secondary fs-5 lh-1">
                                        ${val['user']['name']}
                                    </a>
                                    <p class="fs-7 lh-1 text-muted">${val['date']}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

                document.getElementById("haiku-body").innerHTML += haikuCard;
            })
        })
        .catch(console.error);

    const method = "post";
    const body = JSON.stringify({});
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    fetch("./user/session", { method, headers, body })
        .then((res) => res.json())
        .then((res) => {
            const obj = document.getElementById("navbarDropdown");
            const htmlObj = `
                <img src="/${res['image']}" style="object-fit: cover; width: 2rem; height: 2rem;" class="border rounded-circle mb-1">
                ${res['name']}
            `;
            obj.innerHTML = htmlObj;
        })
}
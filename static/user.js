display();

function favorite(val) {
    const obj = { "id": val };
    const method = "post";
    const body = JSON.stringify(obj);
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    fetch("../haiku/favorite", { method, headers, body }).then((res) => res.json()).then(() => { display(); }).catch(console.error);
}

function del_haiku(val) {
    const obj = { "id": val };
    const method = "post";
    const body = JSON.stringify(obj);
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    fetch("../haiku/delete", { method, headers, body }).then((res) => res.json()).then(() => { display(); }).catch(console.error);
}

function display() {
    const obj = {};
    const method = "post";
    const body = JSON.stringify(obj);
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    fetch(location.pathname, { method, headers, body })
        .then((res) => res.json())
        .then((res) => {
            const userInfo =
                `
                    <div class="text-center">
                        <img src="/${res['image']}" style="object-fit: cover; width: 200px; height: 200px;" class="border border-3 rounded-circle my-3">
                        <h3 class="fw-bold">${res['name']}</h3>
                        <p class="text-muted">@${res['user_id']}</p>
                    </div>
                `
            document.getElementById("user-info").innerHTML = userInfo;
            document.getElementById("haiku-body").innerHTML = "";
            res['haiku'].forEach((val) => {
                let favoriteButton = "";
                if (val['liked']) {
                    favoriteButton =
                        `
                            <button type="button" class="btn ${(val['liked'] == "True") ? "btn btn-primary" : "btn-secondary"} mb-3 favorite" onclick="favorite('${val['id']}')">
                                <i class="${(val['liked'] == "True") ? "fas" : "far"} fa-heart"> ${val['favorite']}</i>
                            </button>
                        `
                }
                let deleteButton = "";
                const obj = {};
                const method = "post";
                const body = JSON.stringify(obj);
                const headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                };
                fetch("../user/session", { method, headers, body }).then((res2) => res2.json()).then((res3) => {
                    if (location.pathname == "/user/" + res3['user_id']) {
                        deleteButton =
                            `
                                <div class="d-flex flex-row-reverse">
                                    <button type="button" class="btn btn-secondary mb-3" onclick="del_haiku('${val['id']}')">
                                        <i class="far fa-trash-alt"></i>
                                    </button>
                                </div>
                            `
                    }
                    const haikuCard =
                        `
                        <div class="card shadow-sm mb-3">
                            <div class="card-body">
                                ${deleteButton}
                                <p class="fs-2 lh-1 text-center mt-3" style="font-family: 'Noto Serif JP', serif;">${val['text']}</p>
                                <div class="text-end">
                                    <div class="row align-items-center d-flex justify-content-between">
                                        <div class="col-auto align-self-end">
                                            ${favoriteButton}
                                        </div>
                                        <div class="col-auto">
                                            <img src="/${res['image']}" style="object-fit: cover; width: 2rem; height: 2rem;" class="border rounded-circle mb-1">
                                            <a href="../user/${res['user_id']}" class="link-secondary fs-5 lh-1">
                                                ${res['name']}
                                            </a>
                                            <p class="fs-7 lh-1 text-muted">${val['date']}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `
                    document.getElementById("haiku-body").innerHTML += haikuCard;
                }).catch(console.error);
            })
        })
}

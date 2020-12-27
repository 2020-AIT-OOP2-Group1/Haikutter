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
    fetch("http://127.0.0.1:5000/user/logout", { method, headers, body })
        .then((res) => res.json())
        .then((res) => {
            if (res["message"] == "Success") {
                location.reload();
            }
        })
        .catch(console.error);
});

const method = "post";
const body = JSON.stringify({});
const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
};
fetch("http://127.0.0.1:5000/user/session", { method, headers, body })
    .then((res) => res.json())
    .then((res) => {
        const obj = document.getElementById("user-header");
        let htmlObj = "";
        if (res['message'] != "Error") {
            htmlObj =
                `
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <div class="d-flex justify-content-end">
                            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                                <div class="dropdown">
                                    <a class="nav-link dropdown-toggle" type="button" id="navbarDropdown" data-toggle="dropdown"
                                        aria-haspopup="true" aria-expanded="false">
                                        <img src="/${res['image']}" style="object-fit: cover; width: 2rem; height: 2rem;" class="border rounded-circle mb-1">
                                        ${res['name']}
                                    </a>
                                    <div class="list-right dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                                        <a class="dropdown-item" href="#exampleModal" data-bs-toggle="modal">Logout</a>
                                    </div>
                                </div>
                            </ul>
                        </div>
                    </div>
                `;
        } else {
            htmlObj =
                `
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <div class="d-flex justify-content-evenly">
                            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                                <li class="nav-item">
                                    <a class="nav-link" href="http://127.0.0.1:5000/login">Login</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                `;
        }
        obj.innerHTML = htmlObj;
    })
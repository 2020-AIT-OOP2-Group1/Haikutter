display();

function display(){
    const obj = {};
    const method = "post";
    const body = JSON.stringify(obj);
    const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    };
    fetch(location.pathname, { method, headers, body })
    .then((res)=> res.json())
    .then((res)=>{
        document.getElementById("haiku-body").innerHTML = "";
        res['haiku'].forEach((val)=>{
            const haikuCard = 
            `
                <div class="card shadow-sm mb-3">
                    <div class="text-end">
                        <div class="row align-items-center d-flex justify-content-between">
                            <div class="col-auto align-self-end">
                                <button type="button" class="btn ${(val['liked'] == "True") ? "btn btn-primary" : "btn-secondary"} mb-3 favorite" onclick="favorite('${val['id']}')">
                                    <i class="${(val['liked'] == "True") ? "fas" : "far"} fa-heart"> ${val['favorite']}</i>
                                </button>
                            </div>
                            <div class="col-auto">
                                <img src="/${val['image']}" style="object-fit: cover; width: 2rem; height: 2rem;" class="border rounded-circle mb-1">
                                <a href="./user/${val['id']}" class="link-secondary fs-5 lh-1">${val['name']}</a>                                    <p class="fs-7 lh-1 text-muted">${val['date']}</p>
                            </div>
                        </div>
                    </div>
                </div>
            `
        document.getElementById("haiku-body").innerHTML += haikuCard;
    })
})
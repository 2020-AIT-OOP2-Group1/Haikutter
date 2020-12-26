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
                    <div class="card-body">
                        <p class="fs-2 lh-1 text-center mt-3">${val['text']}</p>
                        <div class="text-end">
                            <div class="row align-items-center d-flex justify-content-between">
                                <div class="col-auto align-self-end">
                                    <button type="button" class="btn ${(val['liked'] == "True") ? "btn btn-primary" : "btn-secondary"} mb-3 favorite" onclick="favorite('${val['id']}')">
                                        <i class="${(val['liked'] == "True") ? "fas" : "far"} fa-heart"> ${val['favorite']}</i>
                                    </button>
                                </div>
                            </div>
                            <div class="col-auto">
                                <img src="/${res['image']}" style="object-fit: cover; width: 2rem; height: 2rem;" class="border rounded-circle mb-1">
                                <a href="./user/${res['id']}" class="link-secondary fs-5 lh-1">${res['name']}</a>                                    
                                <p class="fs-7 lh-1 text-muted">${val['date']}</p>
                            </div>
                        </div>
                    </div>
                </div>
            `
        document.getElementById("haiku-body").innerHTML += haikuCard;
    })

        document.getElementById("image").innerHTML = "";
        res['haiku'].forEach((val)=>{
            const haikuCard = 
            `
            <img src="/${res['image']}" class="rounded-circle" alt="アイコン" width="180" height="180">
            `
            document.getElementById("image").innerHTML += haikuCard;
    })
})}

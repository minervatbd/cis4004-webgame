const urlBase = "http://127.0.0.1:8000/api";
let userId = localStorage.getItem("userId");

window.onload = () => {
    searchLogs("");
};

async function searchLogs(query) {

    let search = "";
    if (query != "") search = `title=${query}`;

    try {
        let response = await fetch(`${urlBase}/user/${userId}/?${search}`)
        if (response != null) {
            let logs = await response.json()
            if (logs.error) {
                alert("Error searching logs: " + logs.error);
            } else {
                displayLogs(logs || []);
            }
        }
        
    } catch(err) {console.error(err);}
    
}

function displayLogs(logs) {
    const tbody = document.getElementById("logsBody");
    tbody.innerHTML = "";

    if (logs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6">No titles found.</td></tr>`;
        return;
    }
    else{
        logs.forEach((c) => {        
            const row = document.createElement("tr");
            row.innerHTML = `
        <td>${c.title}</td>
        <td>
            <select name="progress" id="${c.id}progress">
                <option value="" selected disabled hidden>${c.progress}</option>
                <option value="Playing">Playing</option>
                <option value="Finished">Finished</option>
                <option value="Completed">Completed</option>
                <option value="Dropped">Dropped</option>
                <option value="Planning">Planning</option>
            </select>
        </td>
        <td>
            <select name="rating" id="${c.id}rating">
                <option value="" selected disabled hidden>${c.rating}</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
            </select>
        </td>
        <td class="table-actions">
            <button onclick='updateLog(${c.id})'>Save changes</button>
            <button onclick='deleteLog(${c.id})'>Remove from library</button>
        </td>
        `;
            tbody.appendChild(row);
    });}
}



async function deleteLog(logId) {
    try {
        let response = await fetch(`${urlBase}/log/${logId}/delete/`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        });
        searchLogs("");
        
    } catch(err) {console.error(err);}
}

async function updateLog(logId) {
    let selectProg = document.getElementById(logId+"progress");
    let prog = selectProg.value;
    let selectRate = document.getElementById(logId+"rating");
    let rate = Number.parseInt(selectRate.value);
    console.log(rate + "  " + prog);

    if (isNaN(rate) && prog == "") return;
    else if (isNaN(rate) && prog != "") {var payload = {progress: prog}; console.log("a");}
    else if (!isNaN(rate) && prog == "") {var payload = {rating: rate}; console.log("b");}
    else {
        var payload = {
            progress: prog,
            rating: rate
        };
         console.log("c");
    }
    alert(JSON.stringify(payload));

    try {
        let response = await fetch(`${urlBase}/log/${logId}/update/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
        });
        alert("Progress/rating updated!");
        searchLogs("");
        
    } catch(err) {console.error(err);}
}
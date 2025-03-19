const urlBase = "http://127.0.0.1:8000/api";
let userId = localStorage.getItem("userId");

window.onload = () => {
    searchGames("");
};

async function searchGames(query) {

    let search = "";
    if (query != "") search = `title=${query}`;

    try {
        let response = await fetch(`${urlBase}/all/?${search}`)
        if (response != null) {
            let games = await response.json()
            if (games.error) {
                alert("Error searching games: " + games.error);
            } else {
                displayGames(games || []);
            }
        }
        
    } catch(err) {console.error(err);}
    
}

function displayGames(games) {
    const tbody = document.getElementById("gamesBody");
    tbody.innerHTML = "";

    if (games.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6">No games found.</td></tr>`;
        return;
    }

    games.forEach(async (c) => {
        let disabled = "";
        
        if (await checkForLog(c.id)) disabled = " disabled";

        const row = document.createElement("tr");
        row.innerHTML = `
      <td>${c.title}</td>
      <td>${c.developer}</td>
      <td>${c.year}</td>
      <td class="table-actions">
        <button onclick="addToCollection(${c.id}, '${c.title}')"${disabled}>Add to library</button>
      </td>
    `;
        tbody.appendChild(row);
    });
}

async function checkForLog(gameId) {
    let response = await fetch(`${urlBase}/log/${userId}/${gameId}/`, {
            method: "GET",
            headers: { "Content-Type": "application/json"},
        });
    return response.ok;
}

function saveGame() {
    const title = document.getElementById("titleInput").value.trim();
    const developer = document.getElementById("developerInput").value.trim();
    const year = document.getElementById("yearInput").value.trim();

    if (!title || !developer || !year) {
        alert("All fields are required");
        return;
    }

    // adding new game
    const payload = {
        title,
        developer,
        year
    }

    fetch(`${urlBase}/create/`, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(payload),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.error) {
                alert("Error adding game: " + data.error);
            } else {
                alert("Added game!")
                }
                searchGames("");
        })
        .catch((err) => console.error(err));
}

async function deleteGame(gameId) {
    const payload = {
        id: gameId,
    };

    try {
        let response = await fetch(`${urlBase}/game/${gameId}/delete/`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        });
        searchGames("");
        
    } catch(err) {console.error(err);}
}

async function addToCollection(gameId, gameTitle) {
    const payload = {
        game_id: gameId,
        title: gameTitle,
        user_id: userId,
        rating: 10,
        progress: "Playing"
    }

    fetch(`${urlBase}/createlog/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.error) {
                alert("Error adding game to collection: " + data.error);
            } else {
                alert("Added game!")
                }
                searchGames("");
        })
        .catch((err) => console.error(err));
}
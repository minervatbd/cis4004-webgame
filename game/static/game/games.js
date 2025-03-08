const urlBase = "http://127.0.0.1:8000/api";
let editingGameId = null;

window.onload = () => {
    searchGames("");
};

function searchGames(query) {
    const payload = {
        search: query
    };

    fetch(`${urlBase}/all/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.error) {
                alert("Error searching games: " + data.error);
            } else {
                displayGames(data.results || []);
            }
        })
        .catch((err) => console.error(err));
}

function displayGames(games) {
    const tbody = document.getElementById("gamesBody");
    tbody.innerHTML = "";

    if (games.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6">No games found.</td></tr>`;
        return;
    }

    contacts.forEach((c) => {
        const row = document.createElement("tr");
        row.innerHTML = `
      <td>${c.title}</td>
      <td>${c.developer}</td>
      <td>${c.year}</td>
      <td class="table-actions">
        <button onclick='deleteGame(${c.ID})'>Delete</button>
      </td>
    `;
        tbody.appendChild(row);
    });
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
        })
        .catch((err) => console.error(err));
}

function deleteGame(gameId) {
    alert(`this button wouldve deleted game id: ${gameId}`);
}
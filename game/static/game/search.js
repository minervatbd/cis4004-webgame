// Function to search for games in your local database
document.addEventListener('DOMContentLoaded', function() {
    // Set up event listener for the search input
    document.getElementById("searchInput").addEventListener("input", function (e) {
        searchGames(e.target.value.trim());
    });

    // Set up event listener for the web search
    document.getElementById("webGameSearchInput").addEventListener("keyup", function(e) {
        if (e.key === "Enter") {
            searchOnlineGame();
        }
    });
});


function searchbarGames(query) {
    // Perform an API call to fetch games based on the search query
    fetch(`/api/games/?title=${query}`)
        .then(response => response.json())
        .then(data => {
            const gamesBody = document.getElementById("gamesBody");
            gamesBody.innerHTML = ''; // Clear the previous results
            data.forEach(game => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${game.title}</td>
                    <td>${game.developer}</td>
                    <td>${game.year}</td>
                    <td>${game.link}</td>
                    <td><button onclick="editGame(${game.id})">Edit</button></td>
                `;
                gamesBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching games:', error));
}

function searchOnlineGame() {
    const query = document.getElementById("webGameSearchInput").value.trim();

    if (query) {
        fetch(`/api/search/?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                const webSearchResults = document.getElementById("webSearchResults");
                webSearchResults.innerHTML = ''; // Clear previous results

                let resultsHtml = "<h3>Search Results:</h3>";

                // Process Steam results
                if (data.steam.length > 0) {
                    resultsHtml += "<h4>Steam</h4><ul>";
                    data.steam.forEach(game => {
                        resultsHtml += `<li>
                            <a href="${game.url}" target="_blank">${game.title}</a>
                            <button onclick="promptAndAddGame('${game.url}', '${game.title}')">Add</button>
                        </li>`;
                    });
                    resultsHtml += "</ul>";
                } else {
                    resultsHtml += "<p>No results found on Steam.</p>";
                }

                // Process Itch.io results
                if (data.itch.length > 0) {
                    resultsHtml += "<h4>Itch.io</h4><ul>";
                    data.itch.forEach(game => {
                        resultsHtml += `<li>
                            <a href="${game.url}" target="_blank">${game.title}</a>
                            <button onclick="promptAndAddGame('${game.url}', '${game.title}')">Add</button>
                        </li>`;
                    });
                    resultsHtml += "</ul>";
                } else {
                    resultsHtml += "<p>No results found on Itch.io.</p>";
                }

                webSearchResults.innerHTML = resultsHtml;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById("webSearchResults").innerHTML = "<p>Error occurred while fetching results.</p>";
            });
    } else {
        alert("Please enter a search term.");
    }
}

// Function to prompt for year and developer before adding the game
function promptAndAddGame(link, title) {
    const developer = prompt("Enter the game's developer:");
    const year = prompt("Enter the game's release year:");

    if (developer && year) {
        // Send the data (title, developer, year) to the backend
        fetch(`${urlBase}/create/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                developer: developer,
                year: year,
                link: link,
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Game added:", data);
            alert(`Game added successfully:\nTitle: ${data.title}\nDeveloper: ${data.developer}\nYear: ${data.year}\nLink: ${data.link}\n`);
        })
        .catch(error => {
            console.error('Error adding game:', error);
            alert("Failed to add game.");
        });
    } else {
        alert("Please provide both the developer and the year.");
    }
}

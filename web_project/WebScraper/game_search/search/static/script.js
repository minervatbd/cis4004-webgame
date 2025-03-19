function sendSearch() {
    const gameName = document.getElementById("gameName").value;
    const platform = document.querySelector('input[name="platform"]:checked').value;

    fetch("/search_game/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()  // Django CSRF token
        },
        body: JSON.stringify({ game: gameName, platform: platform })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.message || "No results found!";
    })
    .catch(error => console.error("Error:", error));
}

// Function to get CSRF Token for Django
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        let [name, value] = cookie.trim().split('=');
        if (name === "csrftoken") return value;
    }
    return "";
}

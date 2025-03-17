let urlBase = "http://127.0.0.1:8000/api";

async function login(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const payload = {
        username: username,
        password: password,
    }
    
    try {
        let response = await fetch(`${urlBase}/login/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        })
        
        // user not found
        if (!response.ok) alert("Invalid username/password!");
        else {
            data = response.json();
            if (data.error) {
                    // Handle error
                    alert(data.error);
                } else {
                    // Handle success
                    alert("Login successful!");
                    localStorage.setItem("userId", data.id);
                    localStorage.setItem("username", data.username);
                    window.location.href = "games";
                }
        }
    } catch(err) {console.error(err);}
}
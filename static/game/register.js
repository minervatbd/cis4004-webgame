const urlBase = "http://127.0.0.1:8000/api";

async function registerUser(event) {
    event.preventDefault();

    const newusername = document.getElementById("username").value;
    const newpassword = document.getElementById("password").value;
    const newemail = document.getElementById("email").value;

    const payload = {
        username: newusername,
        password: newpassword,
        email: newemail
    };

    fetch(`${urlBase}/register/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                alert("Registration successful!");
                localStorage.setItem("userId", data.id);
                localStorage.setItem("username", newusername);
                window.location.href = "games";
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

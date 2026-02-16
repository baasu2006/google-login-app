function register() {
    let username = document.getElementById("username").value;
    let email = document.getElementById("reg_email").value;
    let password = document.getElementById("reg_password").value;

    localStorage.setItem("username", username);
    localStorage.setItem("email", email);
    localStorage.setItem("password", password);

    alert("Registration Successful!");
    window.location.href = "index.html";
}

function login() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    if (
        email === localStorage.getItem("email") &&
        password === localStorage.getItem("password")
    ) {
        window.location.href = "preferences.html";
    } else {
        alert("Invalid Credentials!");
    }
}

function savePreference() {
    let pref = document.getElementById("language").value;
    localStorage.setItem("preference", pref);

    window.location.href = "dashboard.html";
}

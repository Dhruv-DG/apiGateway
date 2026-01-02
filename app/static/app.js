const API_BASE = "";

function hideAll() {
  document.querySelectorAll(".box").forEach(b => b.classList.add("hidden"));
}

function showLogin() {
  hideAll();
  document.getElementById("login-box").classList.remove("hidden");
}

function showRegister() {
  hideAll();
  document.getElementById("register-box").classList.remove("hidden");
}

function showAdmin() {
  hideAll();
  document.getElementById("admin-box").classList.remove("hidden");
}

function showDashboard() {
  hideAll();
  document.getElementById("dashboard").classList.remove("hidden");
}

function login() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  fetch(`/auth/login?email=${email}&password=${password}`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        showDashboard();
      } else {
        document.getElementById("login-status").innerText = "Login failed";
      }
    });
}

function register() {
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;

  fetch(`/auth/register?email=${email}&password=${password}`, { method: "POST" })
    .then(res => res.json())
    .then(() => {
      document.getElementById("register-status").innerText = "Registered. Please login.";
    });
}

function callProtected() {
  const token = localStorage.getItem("token");
  const apiKey = document.getElementById("api-key-input").value;

  const headers = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (apiKey) headers["X-API-Key"] = apiKey;

  fetch(`/protected/data`, { headers })
    .then(async res => ({
      status: res.status,
      body: await res.text()
    }))
    .then(result => {
      document.getElementById("protected-result").innerText =
        `Status: ${result.status}\n${result.body}`;
    });
}

function createApiKey() {
  const token = localStorage.getItem("token");

  fetch(`/keys/create`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("api-key-result").innerText =
        JSON.stringify(data, null, 2);
    });
}

function loadAnalytics() {
  fetch(`/analytics/summary`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("analytics-result").innerText =
        JSON.stringify(data, null, 2);
    });
}

function logout() {
  localStorage.removeItem("token");
  location.reload();
}

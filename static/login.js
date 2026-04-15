const authEl = document.getElementById("auth");
const chatAppEl = document.getElementById("chat-app");
const authStatusEl = document.getElementById("auth-status");
const currentUserEl = document.getElementById("current-user");

function showChatApp(username) {
  authEl.classList.add("hidden");
  chatAppEl.classList.remove("hidden");
  currentUserEl.textContent = `Logged in as ${username}`;
  if (window.ChatApp) {
    window.ChatApp.start();
  }
}

function showAuth() {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  authEl.classList.remove("hidden");
  chatAppEl.classList.add("hidden");
}

async function submitAuth(mode) {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !password) {
    authStatusEl.textContent = "Username and password are required.";
    return;
  }

  authStatusEl.textContent = "Working...";
  try {
    const data = mode === "register"
      ? await API.register(username, password)
      : await API.login(username, password);

    localStorage.setItem("token", data.access_token);
    localStorage.setItem("username", data.user.username);
    authStatusEl.textContent = "Success";
    showChatApp(data.user.username);
  } catch (error) {
    authStatusEl.textContent = error.message;
  }
}

document.getElementById("login-btn").addEventListener("click", () => submitAuth("login"));
document.getElementById("register-btn").addEventListener("click", () => submitAuth("register"));
document.getElementById("logout-btn").addEventListener("click", showAuth);

const savedToken = localStorage.getItem("token");
const savedUsername = localStorage.getItem("username");
if (savedToken && savedUsername) {
  showChatApp(savedUsername);
}

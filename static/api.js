const API = {
  token() {
    return localStorage.getItem("token");
  },

  headers(extra = {}) {
    const token = this.token();
    return {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...extra,
    };
  },

  async request(path, options = {}) {
    const response = await fetch(path, options);
    if (!response.ok) {
      const detail = await response.json().catch(() => ({ detail: "Request failed" }));
      throw new Error(detail.detail || "Request failed");
    }
    return response.json();
  },

  register(username, password) {
    return this.request("/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
  },

  login(username, password) {
    return this.request("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
  },

  getChats() {
    return this.request("/chats", {
      headers: this.headers(),
    });
  },

  getMessages(chatId, sinceId = null) {
    const query = sinceId ? `?chat_id=${chatId}&since_id=${sinceId}` : `?chat_id=${chatId}`;
    return this.request(`/messages${query}`, {
      headers: this.headers(),
    });
  },

  sendMessage(chatId, text, filePath = null) {
    return this.request("/messages", {
      method: "POST",
      headers: this.headers({ "Content-Type": "application/json" }),
      body: JSON.stringify({ chat_id: chatId, text, file_path: filePath }),
    });
  },

  async upload(file) {
    const formData = new FormData();
    formData.append("file", file);
    return this.request("/upload", {
      method: "POST",
      headers: this.headers(),
      body: formData,
    });
  },
};

window.ChatApp = (() => {
  let activeChatId = null;
  let pollTimer = null;
  let lastMessageId = null;

  const chatListEl = document.getElementById("chat-list");
  const messagesEl = document.getElementById("messages");
  const messageInputEl = document.getElementById("message-input");
  const fileInputEl = document.getElementById("file-input");

  function renderMessage(message) {
    const wrapper = document.createElement("div");
    wrapper.className = "message";

    const meta = document.createElement("div");
    const ts = new Date(message.created_at).toLocaleString();
    meta.innerHTML = `<strong>${message.username}</strong> <small>${ts}</small>`;
    wrapper.appendChild(meta);

    if (message.text) {
      const text = document.createElement("div");
      text.textContent = message.text;
      wrapper.appendChild(text);
    }

    if (message.file_path) {
      const img = document.createElement("img");
      img.src = message.file_path;
      img.className = "preview";
      wrapper.appendChild(img);
    }

    messagesEl.appendChild(wrapper);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    lastMessageId = Math.max(lastMessageId || 0, message.id);
  }

  async function loadChats() {
    const chats = await API.getChats();
    chatListEl.innerHTML = "";

    chats.forEach((chat, index) => {
      const btn = document.createElement("button");
      btn.className = "chat-item";
      btn.textContent = chat.name;
      btn.onclick = () => selectChat(chat.id);
      chatListEl.appendChild(btn);

      if (index === 0 && !activeChatId) {
        selectChat(chat.id);
      }
    });
  }

  async function selectChat(chatId) {
    activeChatId = chatId;
    lastMessageId = null;
    messagesEl.innerHTML = "";

    if (pollTimer) {
      clearInterval(pollTimer);
    }

    const messages = await API.getMessages(chatId);
    messages.forEach(renderMessage);

    pollTimer = setInterval(async () => {
      if (!activeChatId) return;
      try {
        const newMessages = await API.getMessages(activeChatId, lastMessageId);
        newMessages.forEach(renderMessage);
      } catch (error) {
        console.error("Polling failed", error);
      }
    }, 2500);
  }

  async function sendMessage() {
    if (!activeChatId) return;

    const text = messageInputEl.value.trim();
    const file = fileInputEl.files[0];

    if (!text && !file) {
      return;
    }

    let filePath = null;
    if (file) {
      const uploadResult = await API.upload(file);
      filePath = uploadResult.file_path;
    }

    const message = await API.sendMessage(activeChatId, text || null, filePath);
    renderMessage(message);

    messageInputEl.value = "";
    fileInputEl.value = "";
  }

  function setupEvents() {
    const sendBtn = document.getElementById("send-btn");
    sendBtn.onclick = () => {
      sendMessage().catch((error) => alert(error.message));
    };

    messageInputEl.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        sendMessage().catch((error) => alert(error.message));
      }
    });
  }

  return {
    async start() {
      setupEvents();
      await loadChats();
    },
  };
})();

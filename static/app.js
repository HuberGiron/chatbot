const chatBox = document.getElementById("chat");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");

const history = [];

function addMessage(text, type = "bot") {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return div;
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const message = messageInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  history.push({ role: "user", content: message });

  messageInput.value = "";
  sendButton.disabled = true;
  messageInput.disabled = true;

  const typingMsg = addMessage("Escribiendo...", "bot typing");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message,
        history
      })
    });

    const data = await response.json();

    typingMsg.remove();

    if (!response.ok) {
      addMessage(data.error || "Ocurrió un error.", "error");
      return;
    }

    addMessage(data.reply, "bot");
    history.push({ role: "assistant", content: data.reply });

  } catch (error) {
    typingMsg.remove();
    addMessage("No se pudo conectar con el servidor.", "error");
  } finally {
    sendButton.disabled = false;
    messageInput.disabled = false;
    messageInput.focus();
  }
});
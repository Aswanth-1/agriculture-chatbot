const chatWidget = document.getElementById("chat-widget");
const chatBackdrop = document.getElementById("chat-backdrop");
const chatToggleButton = document.getElementById("chat-toggle");
const closeChatButton = document.getElementById("close-chat");
const chatLog = document.getElementById("chat-log");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const quickActionsContainer = document.getElementById("quick-actions");
const clearChatButton = document.getElementById("clear-chat");
const openChatButtons = document.querySelectorAll("#hero-open-chat, #hero-open-chat-top, .prompt-open");
const promptButtons = document.querySelectorAll(".chat-trigger");

const state = {
    history: [],
    quickActions: [],
    welcomeLoaded: false,
    isOpen: false,
    isBusy: false,
};

function addMessage(role, text) {
    const message = document.createElement("article");
    message.className = `message ${role}`;
    message.textContent = text;
    chatLog.appendChild(message);
    chatLog.scrollTop = chatLog.scrollHeight;
}

function populateComposer(message = "") {
    messageInput.value = message;
    autoResizeTextarea();
    messageInput.focus();

    const cursorPosition = message.length;
    messageInput.setSelectionRange(cursorPosition, cursorPosition);
}

function autoResizeTextarea() {
    messageInput.style.height = "auto";
    messageInput.style.height = `${Math.min(messageInput.scrollHeight, 180)}px`;
}

function setBusy(isBusy) {
    state.isBusy = isBusy;
    sendButton.disabled = isBusy;
    messageInput.disabled = isBusy;
    clearChatButton.disabled = isBusy;
    sendButton.textContent = isBusy ? "Sending..." : "Send";
}

function setChatOpen(isOpen) {
    state.isOpen = isOpen;
    document.body.classList.toggle("chat-open", isOpen);
    chatWidget.setAttribute("aria-hidden", String(!isOpen));
    chatToggleButton.setAttribute("aria-expanded", String(isOpen));

    if (isOpen) {
        window.setTimeout(() => {
            messageInput.focus();
        }, 120);
    }
}

async function loadWelcomeMessage(forceReset = false) {
    if (forceReset) {
        state.welcomeLoaded = false;
        chatLog.innerHTML = "";
    }

    if (state.welcomeLoaded) {
        return;
    }

    try {
        const response = await fetch("/api/welcome");

        if (!response.ok) {
            throw new Error("Welcome request failed.");
        }

        const data = await response.json();
        state.quickActions = data.quick_actions || [];
        renderQuickActions();
        addMessage("bot", data.message || "Welcome to the agriculture chatbot.");
        state.welcomeLoaded = true;
    } catch (error) {
        if (!chatLog.childElementCount) {
            addMessage("bot", "The chatbot could not load right now. Please try again.");
        }
    }
}

function renderQuickActions() {
    quickActionsContainer.innerHTML = "";

    state.quickActions.forEach((action) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "quick-action";
        button.textContent = action;
        button.addEventListener("click", async () => {
            if (state.isBusy) {
                return;
            }

            await openChatWidget(action, true);
        });
        quickActionsContainer.appendChild(button);
    });
}

async function openChatWidget(initialMessage = "", autoSubmit = false) {
    setChatOpen(true);
    await loadWelcomeMessage();

    if (initialMessage) {
        if (autoSubmit) {
            await submitMessage(initialMessage);
            return;
        }

        populateComposer(initialMessage);
    }
}

function closeChatWidget() {
    setChatOpen(false);
}

async function submitMessage(message) {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || state.isBusy) {
        return;
    }

    if (!state.isOpen) {
        setChatOpen(true);
    }

    addMessage("user", trimmedMessage);
    const requestHistory = [...state.history];
    setBusy(true);

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: trimmedMessage,
                history: requestHistory,
            }),
        });

        if (!response.ok) {
            throw new Error("Chat request failed.");
        }

        const data = await response.json();
        addMessage("bot", data.reply || "I could not generate a response.");
    } catch (error) {
        addMessage("bot", "The website could not reach the chatbot server. Please try again.");
    } finally {
        state.history.push(trimmedMessage);
        setBusy(false);
        populateComposer("");
    }
}

chatToggleButton.addEventListener("click", async () => {
    if (state.isOpen) {
        closeChatWidget();
        return;
    }

    await openChatWidget();
});

closeChatButton.addEventListener("click", closeChatWidget);
chatBackdrop.addEventListener("click", closeChatWidget);

openChatButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        await openChatWidget();
    });
});

promptButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        if (state.isBusy) {
            return;
        }

        const promptText = button.textContent || "";
        await openChatWidget(promptText, true);
    });
});

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await submitMessage(messageInput.value);
});

messageInput.addEventListener("input", autoResizeTextarea);

messageInput.addEventListener("keydown", async (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        await submitMessage(messageInput.value);
    }
});

clearChatButton.addEventListener("click", async () => {
    if (state.isBusy) {
        return;
    }

    state.history = [];
    await loadWelcomeMessage(true);
    populateComposer("");
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && state.isOpen) {
        closeChatWidget();
    }
});

autoResizeTextarea();

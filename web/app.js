// ============================================================
//  app.js – AgriFlow Assistant
//  - toggleChat() / openChat() control the floating widget
//  - sendText() / sendMessage() handle chatbot messages
//  - chatHistory stores only user message strings (never bot)
// ============================================================

var chatHistory = [];
var chatLoaded  = false;   // load welcome only once

// ---- open / close widget ---------------------------------

function toggleChat() {
    var widget = document.getElementById('chatWidget');
    var isOpen = widget.classList.contains('open');

    if (isOpen) {
        widget.classList.remove('open');
    } else {
        widget.classList.add('open');
        // load welcome message the first time chat is opened
        if (!chatLoaded) {
            chatLoaded = true;
            loadWelcome();
        }
        // focus input
        setTimeout(function () {
            document.getElementById('userInput').focus();
        }, 250);
    }
}

// called by hero button and contact button
function openChat() {
    var widget = document.getElementById('chatWidget');
    if (!widget.classList.contains('open')) {
        widget.classList.add('open');
        if (!chatLoaded) {
            chatLoaded = true;
            loadWelcome();
        }
        setTimeout(function () {
            document.getElementById('userInput').focus();
        }, 250);
    }
}

// ---- init ------------------------------------------------
window.onload = function () {
    // Enter key to send
    document.getElementById('userInput')
        .addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
};

// ---- load welcome from /api/welcome ----------------------
function loadWelcome() {
    fetch('/api/welcome')
        .then(function (res) {
            if (!res.ok) throw new Error('Server returned ' + res.status);
            return res.json();
        })
        .then(function (data) {
            if (data && data.message) {
                appendMessage('bot', data.message);
            }
            if (data && Array.isArray(data.quick_actions)) {
                buildQuickActions(data.quick_actions);
            }
        })
        .catch(function (err) {
            console.error('Welcome load error:', err);
            appendMessage('bot',
                'Welcome to AgriFlow Assistant.\n' +
                'Type "help" to see available commands.');
        });
}

// ---- build quick-action buttons --------------------------
function buildQuickActions(actions) {
    var container = document.getElementById('quickActions');
    container.innerHTML = '';
    actions.forEach(function (label) {
        var btn = document.createElement('button');
        btn.className = 'quick-btn';
        btn.textContent = label;
        btn.onclick = function () { sendText(label); };
        container.appendChild(btn);
    });
}

// ---- called by Send button -------------------------------
function sendMessage() {
    var input = document.getElementById('userInput');
    var text  = input.value.trim();
    if (text === '') return;
    input.value = '';
    sendText(text);
}

// ---- core send function ----------------------------------
function sendText(text) {
    if (!text || text.trim() === '') return;
    var message = text.trim();

    appendMessage('user', message);

    var btn = document.getElementById('sendBtn');
    btn.disabled = true;

    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: message,
            history: chatHistory.slice()   // copy, strings only
        })
    })
    .then(function (res) {
        if (!res.ok) throw new Error('HTTP error: ' + res.status);
        return res.json();
    })
    .then(function (data) {
        if (data !== null &&
            data !== undefined &&
            typeof data.reply === 'string') {

            appendMessage('bot', data.reply);
            chatHistory.push(message);   // only user message

        } else {
            console.error('Unexpected response:', data);
            appendMessage('error', 'Received an unexpected response.');
        }
    })
    .catch(function (err) {
        console.error('Chat fetch error:', err);
        appendMessage('error',
            'Could not reach the server.\n' +
            'Make sure web_app.py is running.');
    })
    .finally(function () {
        btn.disabled = false;
        document.getElementById('userInput').focus();
    });
}

// ---- append message bubble -------------------------------
function appendMessage(type, text) {
    var chatBox = document.getElementById('chatBox');
    var div     = document.createElement('div');
    div.className   = 'message ' + type;
    div.textContent = text;          // textContent = safe, no XSS
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

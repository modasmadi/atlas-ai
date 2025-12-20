/**
 * ATLAS AI NOTE - Logic V4
 * Features: Auth Simulation, File Uploads, Multilingual AI, Advanced Formatting
 */

// --- Data Store ---
const Store = {
    getNotes() { const n = localStorage.getItem('atlas-notes'); return n ? JSON.parse(n) : []; },
    saveNotes(n) { localStorage.setItem('atlas-notes', JSON.stringify(n)); },
    getMeta() { const m = localStorage.getItem('atlas-meta'); return m ? JSON.parse(m) : { theme: 'dark' }; },
    saveMeta(m) { localStorage.setItem('atlas-meta', JSON.stringify(m)); },
    getUser() { const u = localStorage.getItem('atlas-user'); return u ? JSON.parse(u) : null; },
    saveUser(u) { localStorage.setItem('atlas-user', JSON.stringify(u)); },

    createNote() {
        const notes = this.getNotes();
        const newNote = { id: Date.now().toString(), title: '', content: '', cover: null, updatedAt: Date.now() };
        notes.unshift(newNote);
        this.saveNotes(notes);
        return newNote;
    },
    updateNote(id, updates) {
        const notes = this.getNotes();
        const idx = notes.findIndex(n => n.id === id);
        if (idx > -1) {
            notes[idx] = { ...notes[idx], ...updates, updatedAt: Date.now() };
            this.saveNotes(notes);
            return notes[idx];
        }
        return null;
    },
    getNote(id) { return this.getNotes().find(n => n.id === id); }
};

// --- App State ---
let activeNoteId = null;

// --- DOM Elements ---
const app = document.getElementById('app');
const loginOverlay = document.getElementById('login-overlay');
const userNameDisplay = document.getElementById('user-name');
const userAvatarDisplay = document.getElementById('user-avatar');

const noteListEl = document.getElementById('note-list');
const addNoteBtn = document.getElementById('add-note-btn');
const editorView = document.getElementById('editor-view');
const emptyState = document.getElementById('empty-state');
const toolbar = document.getElementById('toolbar');

const titleInput = document.getElementById('note-title');
const bodyInput = document.getElementById('note-body');
const coverContainer = document.getElementById('cover-container');
const coverImg = document.getElementById('cover-img');
const addCoverBtn = document.getElementById('add-cover-btn');
const changeCoverBtn = document.querySelector('.change-cover-btn');
const fileInput = document.getElementById('file-upload-input');

const themeBtns = document.querySelectorAll('.theme-btn');
const slashMenu = document.getElementById('slash-menu');

// AI
const aiFab = document.getElementById('ai-fab');
const aiSidebar = document.getElementById('ai-sidebar');
const aiCloseBtn = document.querySelector('.ai-close-btn');
const aiMessages = document.getElementById('ai-messages');
const aiInput = document.getElementById('ai-input');
const aiSendBtn = document.getElementById('ai-send');
const aiAttachBtn = document.getElementById('ai-attach-btn');


// --- Init ---
function init() {
    checkLogin();
    const meta = Store.getMeta();
    setTheme(meta.theme);
    renderNoteList();
    renderEditor();
}

// --- Auth Logic ---
function checkLogin() {
    const user = Store.getUser();
    if (user) {
        loginOverlay.classList.add('hidden');
        userNameDisplay.textContent = user.name;
        userAvatarDisplay.textContent = user.initial;
    } else {
        loginOverlay.classList.remove('hidden');
    }
}

function login(provider) {
    // Simulate Login
    const mockUser = {
        name: provider === 'Apple' ? 'Apple User' : 'M',
        initial: provider === 'Apple' ? '' : 'M',
        provider: provider
    };
    Store.saveUser(mockUser);
    checkLogin();
}

document.getElementById('btn-google').addEventListener('click', () => login('Google'));
document.getElementById('btn-facebook').addEventListener('click', () => login('Facebook'));
document.getElementById('btn-apple').addEventListener('click', () => login('Apple'));


// --- Theme ---
function setTheme(themeName) {
    document.documentElement.setAttribute('data-theme', themeName);
    themeBtns.forEach(btn => {
        if (btn.dataset.setTheme === themeName) btn.classList.add('active');
        else btn.classList.remove('active');
    });
    if (['light', 'dark', 'oled'].includes(themeName)) Store.saveMeta({ theme: themeName });
}
themeBtns.forEach(btn => btn.addEventListener('click', () => setTheme(btn.dataset.setTheme)));

// --- Core Editor ---
function renderNoteList() {
    const notes = Store.getNotes();
    noteListEl.innerHTML = '';
    notes.forEach(note => {
        const li = document.createElement('li');
        li.className = `note-item ${note.id === activeNoteId ? 'active' : ''}`;
        li.innerHTML = `<span class="note-icon">📄</span><span class="note-title-preview">${note.title || 'Untitled'}</span>`;
        if (!note.title) li.querySelector('.note-title-preview').style.opacity = '0.5';
        li.addEventListener('click', () => setActiveNote(note.id));
        noteListEl.appendChild(li);
    });
}

function renderEditor() {
    if (!activeNoteId) {
        editorView.classList.add('hidden');
        toolbar.classList.remove('visible');
        emptyState.classList.remove('hidden');
        return;
    }
    const note = Store.getNote(activeNoteId);
    if (!note) { setActiveNote(null); return; }

    editorView.classList.remove('hidden');
    toolbar.classList.add('visible');
    emptyState.classList.add('hidden');

    if (titleInput.value !== note.title) titleInput.value = note.title || '';
    if (document.activeElement !== bodyInput) bodyInput.innerHTML = note.content || '';

    if (note.cover) {
        coverContainer.classList.add('has-image');
        coverImg.src = note.cover;
        addCoverBtn.style.display = 'none';
    } else {
        coverContainer.classList.remove('has-image');
        addCoverBtn.style.display = 'flex';
    }
}

function setActiveNote(id) {
    activeNoteId = id;
    const note = Store.getNote(id);
    if (note) {
        titleInput.value = note.title || '';
        bodyInput.innerHTML = note.content || '';
        if (!note.title && !note.content) titleInput.focus();
    }
    renderNoteList();
    renderEditor();
}

addNoteBtn.addEventListener('click', () => {
    const newNote = Store.createNote();
    setActiveNote(newNote.id);
});
titleInput.addEventListener('input', (e) => {
    if (activeNoteId) {
        Store.updateNote(activeNoteId, { title: e.target.value });
        const activeItem = document.querySelector(`.note-item[data-id="${activeNoteId}"] .note-title-preview`);
        renderNoteList();
    }
});
bodyInput.addEventListener('input', (e) => {
    if (activeNoteId) Store.updateNote(activeNoteId, { content: e.target.innerHTML });
});

// --- File Upload Logic ---
// We repurpose the single file input for both Cover and Inline Images
let uploadTarget = null; // 'cover' or 'inline'

function handleFileUpload(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const dataUrl = e.target.result;
        if (uploadTarget === 'cover') {
            Store.updateNote(activeNoteId, { cover: dataUrl });
            renderEditor();
        } else if (uploadTarget === 'inline') {
            const html = `<div class="inline-image-wrapper"><img src="${dataUrl}" class="inline-image" contenteditable="false"></div><p><br></p>`;
            document.execCommand('insertHTML', false, html);
        }
    };
    reader.readAsDataURL(file);
}

fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
        handleFileUpload(e.target.files[0]);
    }
    fileInput.value = ''; // reset
});

addCoverBtn.addEventListener('click', () => {
    if (activeNoteId) {
        uploadTarget = 'cover';
        fileInput.click();
    }
});
changeCoverBtn.addEventListener('click', () => {
    if (activeNoteId) {
        uploadTarget = 'cover';
        fileInput.click();
    }
});

// --- Formatting ---
document.querySelectorAll('.tool-btn').forEach(btn => {
    btn.addEventListener('click', () => { document.execCommand(btn.dataset.cmd, false, null); bodyInput.focus(); });
});
document.getElementById('text-color').addEventListener('change', (e) => {
    document.execCommand('foreColor', false, e.target.value);
    bodyInput.focus();
});
document.getElementById('font-family').addEventListener('change', (e) => {
    document.execCommand('fontName', false, e.target.value);
    bodyInput.focus();
});

// --- Slash Command ---
bodyInput.addEventListener('keyup', (e) => { if (e.key === '/') showSlashMenu(); });
document.addEventListener('click', (e) => { if (!slashMenu.contains(e.target) && e.target !== bodyInput) slashMenu.classList.remove('visible'); });

function showSlashMenu() {
    const sel = window.getSelection();
    if (sel.rangeCount > 0) {
        const rect = sel.getRangeAt(0).getBoundingClientRect();
        slashMenu.style.top = `${rect.bottom + window.scrollY}px`;
        slashMenu.style.left = `${rect.left + window.scrollX}px`;
        slashMenu.classList.add('visible');
    }
}

slashMenu.addEventListener('click', (e) => {
    const item = e.target.closest('.slash-item');
    if (!item) return;
    document.execCommand('delete', false, null); // remove slash
    insertBlock(item.dataset.type);
    slashMenu.classList.remove('visible');
});

function insertBlock(type) {
    let html = '';
    switch (type) {
        case 'h1': html = '<h1>Heading 1</h1><p><br></p>'; break;
        case 'h2': html = '<h2>Heading 2</h2><p><br></p>'; break;
        case 'text': html = '<p>Text block</p>'; break;
        case 'todo': html = `<div class="todo-block"><input type="checkbox" class="todo-checkbox"><div class="todo-text" contenteditable="true">To-do item</div></div><p><br></p>`; break;
        case 'bullet': html = `<ul><li>List item</li></ul><p><br></p>`; break;
        case 'callout': html = `<div class="callout-block"><div class="callout-icon">💡</div><div class="callout-content" contenteditable="true">Goal</div></div><p><br></p>`; break;
        case 'calendar': html = generateCalendarWidget(); break;
        case 'bg-yellow':
            document.execCommand('insertHTML', false, '<span class="bg-yellow">Yellow Text</span>&nbsp;');
            return;
        case 'image-upload':
            uploadTarget = 'inline';
            fileInput.click();
            return;
        case 'ai': openAISidebar(); return;
    }
    if (html) document.execCommand('insertHTML', false, html);
}

function generateCalendarWidget() {
    const now = new Date();
    const month = now.toLocaleString('default', { month: 'long' });
    const days = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
    let dHtml = '';
    for (let i = 1; i <= days; i++) dHtml += `<div class="calendar-day ${i === now.getDate() ? 'today' : ''}">${i}</div>`;
    return `<div class="calendar-widget" contenteditable="false"><div class="calendar-header">${month} ${now.getFullYear()}</div><div class="calendar-grid"><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span>${dHtml}</div></div><p><br></p>`;
}

// --- AI Multilingual ---
function openAISidebar() { aiSidebar.classList.add('open'); aiInput.focus(); }
aiCloseBtn.addEventListener('click', () => aiSidebar.classList.remove('open'));
aiFab.addEventListener('click', () => aiSidebar.classList.toggle('open'));
aiSendBtn.addEventListener('click', sendMessage);
aiInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

aiAttachBtn.addEventListener('click', () => {
    // Simulate File selection
    alert("Attach feature simulated: Choose a file to analyze (Dummy Action)");
});

function sendMessage() {
    const text = aiInput.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    aiInput.value = '';
    setTimeout(() => {
        addMessage(generateAIResponse(text), 'bot');
    }, 600);
}

function addMessage(text, sender) {
    const d = document.createElement('div');
    d.className = `ai-msg ${sender}`;
    d.textContent = text;
    aiMessages.appendChild(d);
    aiMessages.scrollTop = aiMessages.scrollHeight;
}

function generateAIResponse(input) {
    const isArabic = /[\u0600-\u06FF]/.test(input);
    const lower = input.toLowerCase();

    if (isArabic) {
        if (lower.includes('مرحبا') || lower.includes('السلام')) return "أهلاً بك في أطلس! كيف يمكنني مساعدتك اليوم؟";
        if (lower.includes('اسمك')) return "أنا أطلس، مساعدك الذكي.";
        if (lower.includes('صورة')) return "لإضافة صورة، اكتب '/' واختر 'Upload Image'.";
        if (lower.includes('تقويم')) return "يمكنك إضافة تقويم بكتابة '/calendar'.";
        return "هذا مثير للاهتمام! أنا حالياً في النسخة التجريبية، لكن يمكنني مساعدتك في تنظيم ملاحظاتك.";
    }

    if (lower.includes('hello') || lower.includes('hi')) return "Hello! I am ATLAS. How can I assist you?";
    if (lower.includes('goal')) return "Try using the '/callout' command for goals!";
    if (lower.includes('calendar')) return "Type '/calendar' to insert a widget.";
    if (lower.includes('upload')) return "You can upload images using the slash menu!";
    return "I'm here to help you navigate ATLAS. Try asking about features!";
}

init();

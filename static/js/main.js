/**
 * FAUNA & FLORA — Asosiy Interaktiv Skript
 * Web Audio Tovush Sintezi, AI Yordamchi, Kirish Animatsiyasi
 */

// 1. WEB AUDIO SINTEZI VA AUDIO PLAYER
class AnimalAudioEngine {
    constructor() {
        this.audioCtx = null;
        this.currentAudio = null;
        this.currentBtn = null;
    }

    initContext() {
        if (!this.audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.audioCtx = new AudioContext();
        }
        if (this.audioCtx.state === 'suspended') {
            this.audioCtx.resume();
        }
    }

    playSound(soundType, audioUrl, buttonEl) {
        this.initContext();

        // Agar hozir biror ovoz o'ynayotgan bo'lsa, to'xtatish
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio = null;
        }
        if (this.currentBtn) {
            this.currentBtn.classList.remove('playing');
        }

        if (this.currentBtn === buttonEl) {
            this.currentBtn = null;
            return; // Ikkinchi marta bosilganda o'chirish
        }

        buttonEl.classList.add('playing');
        this.currentBtn = buttonEl;

        // Agar audio fayli mavjud bo'lsa, uni o'ynatishga urinish
        if (audioUrl && audioUrl.endsWith('.mp3')) {
            const audio = new Audio(audioUrl);
            this.currentAudio = audio;
            audio.play().then(() => {
                audio.onended = () => {
                    buttonEl.classList.remove('playing');
                    this.currentBtn = null;
                    this.currentAudio = null;
                };
            }).catch(() => {
                // Audio fayl topilmasa yoki xatolik bersa, Web Audio sintezatoriga o'tish
                this.synthesizeAnimalSound(soundType, buttonEl);
            });
        } else {
            this.synthesizeAnimalSound(soundType, buttonEl);
        }
    }

    // Har bir hayvon uchun fizik va akustik tovush sintezi
    synthesizeAnimalSound(type, buttonEl) {
        const ctx = this.audioCtx;
        const now = ctx.currentTime;

        const cleanup = (duration) => {
            setTimeout(() => {
                buttonEl.classList.remove('playing');
                if (this.currentBtn === buttonEl) this.currentBtn = null;
            }, duration * 1000);
        };

        if (type === 'lion') {
            // Sherning chuqur vahimali o'kirishi (past chastotali modulyatsiyalangan rezonans)
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            const filter = ctx.createBiquadFilter();

            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(110, now);
            osc.frequency.exponentialRampToValueAtTime(55, now + 1.2);
            osc.frequency.exponentialRampToValueAtTime(40, now + 2.5);

            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(400, now);
            filter.frequency.linearRampToValueAtTime(180, now + 2.5);

            gain.gain.setValueAtTime(0, now);
            gain.gain.linearRampToValueAtTime(0.7, now + 0.3);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 2.5);

            osc.connect(filter);
            filter.connect(gain);
            gain.connect(ctx.destination);

            osc.start(now);
            osc.stop(now + 2.5);
            cleanup(2.5);

        } else if (type === 'swallow') {
            // Qaldirg'ochning quvnoq va ohangdor sayrashi (chirp/trill)
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sine';
            for (let i = 0; i < 6; i++) {
                const t = now + (i * 0.25);
                osc.frequency.setValueAtTime(2400, t);
                osc.frequency.exponentialRampToValueAtTime(3800, t + 0.1);
                osc.frequency.exponentialRampToValueAtTime(2100, t + 0.2);
            }

            gain.gain.setValueAtTime(0.3, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 1.6);

            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.start(now);
            osc.stop(now + 1.6);
            cleanup(1.6);

        } else if (type === 'wolf') {
            // Bo'rining cho'ziq mungli uvillashi (harmonic sweep)
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'triangle';
            osc.frequency.setValueAtTime(320, now);
            osc.frequency.linearRampToValueAtTime(540, now + 1.2);
            osc.frequency.linearRampToValueAtTime(420, now + 2.4);
            osc.frequency.exponentialRampToValueAtTime(260, now + 3.2);

            gain.gain.setValueAtTime(0, now);
            gain.gain.linearRampToValueAtTime(0.5, now + 0.5);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 3.2);

            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.start(now);
            osc.stop(now + 3.2);
            cleanup(3.2);

        } else if (type === 'eagle') {
            // Burgutning o'tkir qichqirig'i
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(1800, now);
            osc.frequency.exponentialRampToValueAtTime(2900, now + 0.4);
            osc.frequency.exponentialRampToValueAtTime(900, now + 1.5);

            gain.gain.setValueAtTime(0.4, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 1.5);

            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.start(now);
            osc.stop(now + 1.5);
            cleanup(1.5);

        } else if (type === 'dolphin') {
            // Delfinning sonik chertishlari
            for (let i = 0; i < 12; i++) {
                const clickOsc = ctx.createOscillator();
                const clickGain = ctx.createGain();
                const t = now + (i * 0.08);

                clickOsc.type = 'sine';
                clickOsc.frequency.setValueAtTime(4000 + Math.random() * 2000, t);
                clickGain.gain.setValueAtTime(0.2, t);
                clickGain.gain.exponentialRampToValueAtTime(0.001, t + 0.04);

                clickOsc.connect(clickGain);
                clickGain.connect(ctx.destination);
                clickOsc.start(t);
                clickOsc.stop(t + 0.04);
            }
            cleanup(1.2);

        } else {
            // Standart tovush (quyon ogohlantirish signali / yumshoq zarba)
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(440, now);
            osc.frequency.exponentialRampToValueAtTime(220, now + 0.6);

            gain.gain.setValueAtTime(0.4, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.6);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 0.6);
            cleanup(0.6);
        }
    }
}

const audioEngine = new AnimalAudioEngine();

// 2. AI ASSISTANT CHAT ENGINE
class FaunaAIChat {
    constructor() {
        this.chatBox = document.getElementById('aiMessagesContainer');
        this.inputEl = document.getElementById('aiChatInput');
        this.btnEl = document.getElementById('aiSendBtn');
        this.init();
    }

    init() {
        if (!this.inputEl || !this.btnEl) return;

        this.btnEl.addEventListener('click', () => this.sendMessage());
        this.inputEl.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    async sendMessage() {
        const text = this.inputEl.value.trim();
        if (!text) return;

        this.appendMessage('user', text);
        this.inputEl.value = '';

        // Typing indikatori
        const typingId = this.appendTypingIndicator();

        try {
            const resp = await fetch('/api/ai/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await resp.json();
            this.removeTypingIndicator(typingId);
            this.appendMessage('assistant', data.answer);
        } catch (err) {
            this.removeTypingIndicator(typingId);
            this.appendMessage('assistant', 'Kechirasiz, javob olishda xatolik yuz berdi. Iltimos, qaytadan urinib ko\'ring.');
        }
    }

    appendMessage(role, text) {
        if (!this.chatBox) return;
        const bubble = document.createElement('div');
        bubble.className = `chat-bubble ${role}`;
        // Oddiy markdown formatlashni o'girish
        let formatted = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code style="background:rgba(0,0,0,0.3);padding:2px 6px;border-radius:4px;">$1</code>')
            .replace(/\n/g, '<br>');
        bubble.innerHTML = formatted;
        this.chatBox.appendChild(bubble);
        this.chatBox.scrollTop = this.chatBox.scrollHeight;
    }

    appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const bubble = document.createElement('div');
        bubble.id = id;
        bubble.className = 'chat-bubble assistant';
        bubble.innerHTML = '<em>Fauna AI o\'ylamoqda... 🐾</em>';
        this.chatBox.appendChild(bubble);
        this.chatBox.scrollTop = this.chatBox.scrollHeight;
        return id;
    }

    removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }
}

// 3. SAHIFA YUKLANGANDA ISHGA TUSHUVCHI HODISALAR
document.addEventListener('DOMContentLoaded', () => {
    // A. AI Entrance Splash Animatsiyasi (Bir marta ko'rsatiladi va yo'qoladi)
    const splash = document.getElementById('aiSplashOverlay');
    if (splash) {
        setTimeout(() => {
            splash.classList.add('hidden');
        }, 1200);
    }

    // B. Audio tinglash tugmalarini ulash
    document.querySelectorAll('.btn-sound-play').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const soundType = btn.getAttribute('data-sound-type') || 'roar';
            const audioUrl = btn.getAttribute('data-sound-file') || '';
            audioEngine.playSound(soundType, audioUrl, btn);
        });
    });

    // C. AI Chatni ishga tushirish
    new FaunaAIChat();

    // D. Tezkor farq modalini ochish
    window.openDiffModal = function(name, diffText, similarSpecies) {
        const modal = document.getElementById('speciesDiffModal');
        if (!modal) return;
        document.getElementById('modalAnimalName').innerText = name;
        document.getElementById('modalSimilarSpecies').innerText = similarSpecies;
        document.getElementById('modalDiffBody').innerHTML = diffText.replace(/\n/g, '<br>');
        modal.style.display = 'flex';
    };

    window.closeDiffModal = function() {
        const modal = document.getElementById('speciesDiffModal');
        if (modal) modal.style.display = 'none';
    };
});

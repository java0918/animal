/**
 * ZOOVENTURE — Login va Parol orqali Kirish Tizimi
 */

function submitLogin(e) {
    if (e) e.preventDefault();

    const userInput = document.getElementById('login_user');
    const passInput = document.getElementById('login_pass');
    const errorEl = document.getElementById('loginError');
    const btn = document.getElementById('btnLoginSubmit');

    const username = userInput ? userInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';

    if (!username || !password) {
        if (errorEl) {
            errorEl.innerText = "Iltimos, login va parolni to'liq kiriting!";
            errorEl.style.display = 'block';
        }
        return;
    }

    if (btn) {
        btn.disabled = true;
        btn.innerHTML = 'Tekshirilmoqda... ⏳';
    }
    if (errorEl) errorEl.style.display = 'none';

    fetch('/api/auth/admin-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const isAdmin = data.role === 'admin' || (data.user && data.user.role === 'admin');
            const msg = isAdmin ? "ADMIN TASDIQLANDI... BOSHQARUV PANELIGA O'TILMOQDA!" : 'TASDIQLANDI... XUSH KELIBSIZ!';
            playEntranceTransition(msg, data.redirect || (isAdmin ? '/admin' : '/'));
        } else {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = 'Tizimga Kirish 🔓';
            }
            if (errorEl) {
                errorEl.innerText = data.message || "Login yoki parol noto'g'ri!";
                errorEl.style.display = 'block';
                errorEl.animate([
                    { transform: 'translateX(-6px)' },
                    { transform: 'translateX(6px)' },
                    { transform: 'translateX(-4px)' },
                    { transform: 'translateX(4px)' },
                    { transform: 'translateX(0)' }
                ], { duration: 300 });
            }
        }
    })
    .catch(() => {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = 'Tizimga Kirish 🔓';
        }
        if (errorEl) {
            errorEl.innerText = "Server bilan aloqa xatosi! Qaytadan urinib ko'ring.";
            errorEl.style.display = 'block';
        }
    });
}

function loginAsDemo(role, e) {
    const btn = (e && e.target) || (window.event ? window.event.target : null);
    if (btn) btn.innerHTML = 'Kirilmoqda... ⏳';

    fetch('/api/auth/demo-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: 'user' })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            playEntranceTransition('MEHMON SIFATIDA IDENTIFIKATSIYA QILINDI...', data.redirect || '/');
        } else {
            alert('Kirishda xatolik: ' + (data.message || ''));
            if (btn) btn.innerHTML = "⚡ Demo Access";
        }
    })
    .catch(err => {
        console.error('Demo login error:', err);
        alert("Server bilan bog'lanishda xatolik yuz berdi.");
        if (btn) btn.innerHTML = "⚡ Demo Access";
    });
}

function playEntranceTransition(customText, customRedirect) {
    const overlay = document.getElementById('aiSplashOverlay');
    if (overlay) {
        overlay.classList.remove('hidden');
        const status = overlay.querySelector('.ai-status-text');
        if (status) status.innerText = customText || 'AI IDENTIFIKATSIYA TASDIQLANDI... XUSH KELIBSIZ!';
    }
    setTimeout(() => {
        if (customRedirect) {
            window.location.href = customRedirect;
            return;
        }
        const urlParams = new URLSearchParams(window.location.search);
        const redirect = urlParams.get('redirect') || '/';
        window.location.href = redirect;
    }, 1200);
}

window.onload = function() {
    const userInput = document.getElementById('login_user');
    if (userInput) userInput.focus();
};

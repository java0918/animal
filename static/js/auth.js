/**
 * FAUNA & FLORA — Google Sign-In & Auth Tizimi
 */

function handleCredentialResponse(response) {
    // Google One Tap yoki Google Sign-In orqali olingan JWT token
    fetch('/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ credential: response.credential })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            playEntranceTransition();
        } else {
            alert('Google orqali kirishda xatolik: ' + (data.message || 'Noma\'lum xatolik'));
        }
    })
    .catch(err => {
        alert('Server bilan bog\'lanishda xatolik.');
    });
}

function loginAsDemo(role) {
    const btn = event ? event.target : null;
    if (btn) btn.innerHTML = 'Kirilmoqda... ⏳';

    fetch('/api/auth/demo-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: role })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            playEntranceTransition();
        } else {
            alert('Kirishda xatolik');
            if (btn) btn.innerHTML = role === 'admin' ? '🛡️ Admin sifatida kirish' : '👤 Foydalanuvchi sifatida';
        }
    })
    .catch(err => {
        alert('Server xatosi');
    });
}

function playEntranceTransition() {
    const overlay = document.getElementById('aiSplashOverlay');
    if (overlay) {
        overlay.classList.remove('hidden');
        const status = overlay.querySelector('.ai-status-text');
        if (status) status.innerText = 'AI IDENTIFIKATSIYA TASDIQLANDI... XUSH KELIBSIZ!';
    }
    setTimeout(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const redirect = urlParams.get('redirect') || '/';
        window.location.href = redirect;
    }, 1200);
}

// Google Identity Services ishga tushirish
window.onload = function() {
    const googleClientIdEl = document.getElementById('googleClientIdData');
    const clientId = googleClientIdEl ? googleClientIdEl.value : '';

    if (clientId && window.google) {
        google.accounts.id.initialize({
            client_id: clientId,
            callback: handleCredentialResponse
        });
        const googleBtnParent = document.getElementById('googleSignInBtnWrap');
        if (googleBtnParent) {
            google.accounts.id.renderButton(
                googleBtnParent,
                { theme: "outline", size: "large", width: "100%", text: "continue_with" }
            );
        }
    }
};

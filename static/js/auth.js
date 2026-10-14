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
}

function toggleAdminLoginForm(show) {
    const userBlock = document.getElementById('userLoginBlock');
    const adminBlock = document.getElementById('adminLoginBlock');
    if (userBlock && adminBlock) {
        userBlock.style.display = show ? 'none' : 'block';
        adminBlock.style.display = show ? 'block' : 'none';
        if (show) {
            const userInput = document.getElementById('admin_login_user');
            if (userInput) userInput.focus();
        }
    }
}

function loginAsAdmin(e) {
    if (e) e.preventDefault();
    const username = document.getElementById('admin_login_user').value.trim();
    const password = document.getElementById('admin_login_pass').value.trim();
    const errorEl = document.getElementById('adminLoginError');
    const btn = document.getElementById('btnSubmitAdminLogin');

    if (!username || !password) {
        if (errorEl) {
            errorEl.innerText = 'Login va parolni kiriting!';
            errorEl.style.display = 'block';
        }
        return;
    }

    btn.disabled = true;
    btn.innerText = 'Tekshirilmoqda... ⏳';
    if (errorEl) errorEl.style.display = 'none';

    fetch('/api/auth/admin-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const overlay = document.getElementById('aiSplashOverlay');
            if (overlay) {
                overlay.classList.remove('hidden');
                const status = overlay.querySelector('.ai-status-text');
                if (status) status.innerText = 'ADMIN TASDIQLANDI... XUSH KELIBSIZ!';
            }
            setTimeout(() => {
                window.location.href = data.redirect || '/admin';
            }, 1000);
        } else {
            btn.disabled = false;
            btn.innerText = 'Kirish 🔓';
            if (errorEl) {
                errorEl.innerText = data.message || 'Login yoki parol xato!';
                errorEl.style.display = 'block';
            }
        }
    })
    .catch(() => {
        btn.disabled = false;
        btn.innerText = 'Kirish 🔓';
        if (errorEl) {
            errorEl.innerText = 'Server bilan aloqa xatosi!';
            errorEl.style.display = 'block';
        }
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

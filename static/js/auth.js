/**
 * FAUNA & FLORA — 2-Bosqichli Google & Login-Parol Auth Tizimi
 */

function goToStep(stepNumber) {
    const pill1 = document.getElementById('stepPill1');
    const pill2 = document.getElementById('stepPill2');
    const block1 = document.getElementById('step1Block');
    const block2 = document.getElementById('step2Block');

    if (stepNumber === 1) {
        if (pill1) pill1.classList.add('active');
        if (pill2) pill2.classList.remove('active');
        if (block1) block1.style.display = 'block';
        if (block2) block2.style.display = 'none';
    } else if (stepNumber === 2) {
        if (pill2) pill2.classList.add('active');
        if (pill1) pill1.classList.remove('active');
        if (block1) block1.style.display = 'none';
        if (block2) block2.style.display = 'block';

        const emailInput = document.getElementById('googleEmailInput');
        const displayEl = document.getElementById('step2GoogleDisplay');
        const selectedEmail = (emailInput && emailInput.value.trim()) ? emailInput.value.trim() : 'admin@hayvonlar.uz';
        if (displayEl) displayEl.innerText = selectedEmail;

        const passInput = document.getElementById('step2_login_pass');
        if (passInput) passInput.focus();
    }
}

function proceedToStep2WithGoogle() {
    goToStep(2);
}

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
            playEntranceTransition('GOOGLE IDENTIFIKATSIYA TASDIQLANDI... XUSH KELIBSIZ!');
        } else {
            alert('Google orqali kirishda xatolik: ' + (data.message || 'Noma\'lum xatolik'));
        }
    })
    .catch(() => {
        alert('Server bilan bog\'lanishda xatolik yuz berdi.');
    });
}

function submitStep2Login(e) {
    if (e) e.preventDefault();
    const userInput = document.getElementById('step2_login_user');
    const passInput = document.getElementById('step2_login_pass');
    const emailInput = document.getElementById('googleEmailInput');
    const errorEl = document.getElementById('step2Error');
    const btn = document.getElementById('btnSubmitStep2');

    const username = userInput ? userInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';
    const googleEmail = emailInput ? emailInput.value.trim() : 'admin@hayvonlar.uz';

    if (!username || !password) {
        if (errorEl) {
            errorEl.innerText = 'Iltimos, login va parolni to\'liq kiriting!';
            errorEl.style.display = 'block';
        }
        return;
    }

    if (btn) {
        btn.disabled = true;
        btn.innerHTML = 'Tekshirilmoqda... ⏳';
    }
    if (errorEl) errorEl.style.display = 'none';

    fetch('/api/auth/step2-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: username,
            password: password,
            google_email: googleEmail
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const isAdmin = data.role === 'admin' || (data.user && data.user.role === 'admin');
            const msg = isAdmin ? 'ADMIN TASDIQLANDI... BOSHQARUV PANELIGA O\'TILMOQDA!' : 'TASDIQLANDI... XUSH KELIBSIZ!';
            playEntranceTransition(msg, data.redirect || (isAdmin ? '/admin' : '/'));
        } else {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = 'Tizimga Kirish 🔓';
            }
            if (errorEl) {
                errorEl.innerText = data.message || 'Login yoki parol xato!';
                errorEl.style.display = 'block';
            }
        }
    })
    .catch(() => {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = 'Tizimga Kirish 🔓';
        }
        if (errorEl) {
            errorEl.innerText = 'Server bilan aloqa xatosi! Qaytadan urinib ko\'ring.';
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
        body: JSON.stringify({ role: role })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            playEntranceTransition('MEHMON SIFATIDA IDENTIFIKATSIYA QILINDI...');
        } else {
            alert('Kirishda xatolik: ' + (data.message || ''));
            if (btn) btn.innerHTML = '⚡ Mehmon sifatida tezkor ko\'rish';
        }
    })
    .catch(err => {
        console.error('Demo login error:', err);
        alert('Server bilan bog\'lanishda xatolik yuz berdi.');
        if (btn) btn.innerHTML = '⚡ Mehmon sifatida tezkor ko\'rish';
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

// Google Identity Services & Sahifa yuklanganda qadamni tekshirish
window.onload = function() {
    const params = new URLSearchParams(window.location.search);
    if (params.get('step') === '2' || params.get('redirect') === '/admin' || params.get('admin') === '1') {
        goToStep(2);
    }

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

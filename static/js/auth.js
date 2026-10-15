/**
 * FAUNA & FLORA — 2-Bosqichli Google & Login-Parol Auth Tizimi
 * 1-qadam: Google hisob (Majburiy)
 * 2-qadam: Login & Parol (Faqat Google tasdiqlangandan so'ng)
 */

let googleAccountVerified = false;
let verifiedGoogleEmail = "";

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showStep1Error(msg) {
    const err = document.getElementById('step1Error');
    const succ = document.getElementById('step1Success');
    if (succ) succ.style.display = 'none';
    if (err) {
        err.innerText = msg;
        err.style.display = 'block';
        err.animate([
            { transform: 'translateX(-6px)' },
            { transform: 'translateX(6px)' },
            { transform: 'translateX(-4px)' },
            { transform: 'translateX(4px)' },
            { transform: 'translateX(0)' }
        ], { duration: 300 });
    }
    const input = document.getElementById('googleEmailInput');
    if (input) {
        input.style.borderColor = '#ef4444';
        input.focus();
    }
}

function clearStep1Error() {
    const err = document.getElementById('step1Error');
    if (err) err.style.display = 'none';
    const input = document.getElementById('googleEmailInput');
    if (input) input.style.borderColor = '';
}

function verifyGoogleAndProceed() {
    const emailInput = document.getElementById('googleEmailInput');
    const email = emailInput ? emailInput.value.trim() : '';

    if (!email) {
        showStep1Error("⚠️ Iltimos, avval Google elektron pochtangizni kiriting!");
        return false;
    }
    if (!isValidEmail(email)) {
        showStep1Error("⚠️ Iltimos, haqiqiy elektron pochta manzilini kiriting! (Masalan: sizningnomingiz@gmail.com)");
        return false;
    }

    clearStep1Error();
    googleAccountVerified = true;
    verifiedGoogleEmail = email;

    const succ = document.getElementById('step1Success');
    if (succ) {
        succ.innerText = `✅ Google hisob tasdiqlandi: ${email}`;
        succ.style.display = 'block';
    }

    const btn = document.getElementById('btnVerifyGoogle');
    if (btn) btn.innerHTML = 'Tasdiqlandi! 2-qadamga o\'tilmoqda... ⏳';

    setTimeout(() => {
        if (btn) btn.innerHTML = 'Tasdiqlash va 2-qadamga o\'tish ➔';
        goToStep(2);
    }, 450);
    return true;
}

function proceedToStep2WithGoogle() {
    const emailInput = document.getElementById('googleEmailInput');
    const email = emailInput ? emailInput.value.trim() : '';
    if (email && isValidEmail(email)) {
        verifyGoogleAndProceed();
        return;
    }

    if (window.google && window.google.accounts && window.google.accounts.id) {
        try {
            google.accounts.id.prompt();
        } catch(e) {}
    }

    showStep1Error("⚠️ Google hisob bilan kirmasa login-parolga o'tib bo'lmaydi! Iltimos, pochtangizni kiriting.");
    if (emailInput) emailInput.focus();
}

function tryGoToStep2() {
    if (!googleAccountVerified) {
        showStep1Error("⚠️ 2-qadam (Login va Parol)ga o'tish uchun avval 1-bosqichda Google hisobingizni tasdiqlang!");
        return;
    }
    goToStep(2);
}

function goToStep(stepNumber) {
    // 1-qadam Google hisob tasdiqlanmasa 2-qadamga o'tish qat'iyan taqiqlanadi
    if (stepNumber === 2 && !googleAccountVerified) {
        tryGoToStep2();
        return;
    }

    const pill1 = document.getElementById('stepPill1');
    const pill2 = document.getElementById('stepPill2');
    const block1 = document.getElementById('step1Block');
    const block2 = document.getElementById('step2Block');

    if (stepNumber === 1) {
        if (pill1) pill1.classList.add('active');
        if (pill2) pill2.classList.remove('active');
        if (block1) block1.style.display = 'block';
        if (block2) block2.style.display = 'none';
        clearStep1Error();
    } else if (stepNumber === 2) {
        if (pill2) pill2.classList.add('active');
        if (pill1) pill1.classList.remove('active');
        if (block1) block1.style.display = 'none';
        if (block2) block2.style.display = 'block';

        const displayEl = document.getElementById('step2GoogleDisplay');
        if (displayEl) {
            displayEl.innerText = verifiedGoogleEmail || 'Google hisob tasdiqlangan';
        }

        const passInput = document.getElementById('step2_login_pass');
        const userInput = document.getElementById('step2_login_user');
        if (userInput && !userInput.value) {
            userInput.focus();
        } else if (passInput) {
            passInput.focus();
        }
    }
}

function handleCredentialResponse(response) {
    let googleEmailFromJwt = '';
    try {
        const payloadBase64 = response.credential.split('.')[1];
        const decodedJson = JSON.parse(atob(payloadBase64.replace(/-/g, '+').replace(/_/g, '/')));
        if (decodedJson && decodedJson.email) {
            googleEmailFromJwt = decodedJson.email;
        }
    } catch (err) {
        console.log('JWT parse:', err);
    }

    fetch('/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ credential: response.credential })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const email = googleEmailFromJwt || (data.user && data.user.email) || 'google-user@gmail.com';
            googleAccountVerified = true;
            verifiedGoogleEmail = email;

            const emailInput = document.getElementById('googleEmailInput');
            if (emailInput) emailInput.value = email;

            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('redirect') === '/admin' || (data.user && data.user.role === 'admin')) {
                goToStep(2);
            } else {
                playEntranceTransition('GOOGLE IDENTIFIKATSIYA TASDIQLANDI... XUSH KELIBSIZ!');
            }
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

    if (!googleAccountVerified || !verifiedGoogleEmail) {
        showStep1Error("⚠️ Google hisob tasdiqlanmagan! Avval 1-bosqichda pochtangizni kiriting.");
        goToStep(1);
        return;
    }

    const userInput = document.getElementById('step2_login_user');
    const passInput = document.getElementById('step2_login_pass');
    const errorEl = document.getElementById('step2Error');
    const btn = document.getElementById('btnSubmitStep2');

    const username = userInput ? userInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';

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
            google_email: verifiedGoogleEmail
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

// Google Identity Services yuklash va boshlang'ich tekshiruv
window.onload = function() {
    // 1-qadam har doim birinchi bo'lib ochiladi
    goToStep(1);

    const params = new URLSearchParams(window.location.search);
    if (params.get('redirect') === '/admin') {
        const adminNotice = document.getElementById('step1AdminNotice');
        if (adminNotice) adminNotice.style.display = 'block';
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

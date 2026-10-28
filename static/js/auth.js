/**
 * ZOOVENTURE — Foydalanuvchi va Admin Kirish / Ro'yxatdan o'tish tizimi
 */

// Tablar orasida o'tish (Tizimga kirish <-> Ro'yxatdan o'tish)
function switchAuthTab(tab) {
    const tabLogin = document.getElementById('tabBtnLogin');
    const tabRegister = document.getElementById('tabBtnRegister');
    const formLogin = document.getElementById('formLogin');
    const formRegister = document.getElementById('formRegister');
    const loginError = document.getElementById('loginError');
    const registerError = document.getElementById('registerError');
    const registerSuccess = document.getElementById('registerSuccess');

    if (loginError) loginError.style.display = 'none';
    if (registerError) registerError.style.display = 'none';
    if (registerSuccess) registerSuccess.style.display = 'none';

    if (tab === 'register') {
        if (formLogin) formLogin.style.display = 'none';
        if (formRegister) {
            formRegister.style.display = 'block';
            formRegister.animate([
                { opacity: 0, transform: 'translateY(8px)' },
                { opacity: 1, transform: 'translateY(0)' }
            ], { duration: 250, fill: 'forwards' });
        }

        if (tabRegister) {
            tabRegister.style.background = '#10b981';
            tabRegister.style.color = '#ffffff';
            tabRegister.style.boxShadow = '0 2px 10px rgba(16, 185, 129, 0.4)';
        }
        if (tabLogin) {
            tabLogin.style.background = 'transparent';
            tabLogin.style.color = '#94a3b8';
            tabLogin.style.boxShadow = 'none';
        }

        const regUser = document.getElementById('reg_user');
        if (regUser && !regUser.value) regUser.focus();
    } else {
        if (formRegister) formRegister.style.display = 'none';
        if (formLogin) {
            formLogin.style.display = 'block';
            formLogin.animate([
                { opacity: 0, transform: 'translateY(8px)' },
                { opacity: 1, transform: 'translateY(0)' }
            ], { duration: 250, fill: 'forwards' });
        }

        if (tabLogin) {
            tabLogin.style.background = '#10b981';
            tabLogin.style.color = '#ffffff';
            tabLogin.style.boxShadow = '0 2px 10px rgba(16, 185, 129, 0.4)';
        }
        if (tabRegister) {
            tabRegister.style.background = 'transparent';
            tabRegister.style.color = '#94a3b8';
            tabRegister.style.boxShadow = 'none';
        }

        const loginUser = document.getElementById('login_user');
        const loginPass = document.getElementById('login_pass');
        if (loginUser && loginUser.value && loginPass) {
            loginPass.focus();
        } else if (loginUser) {
            loginUser.focus();
        }
    }
}

// Parolni ko'rsatish yoki yashirish
function togglePasswordVisibility(inputId, triggerEl) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const isPass = input.type === 'password';
    input.type = isPass ? 'text' : 'password';
    if (triggerEl) {
        triggerEl.innerHTML = isPass ? 'Yashirish 🔒' : "Ko'rsatish 👁️";
    }
}

// Foydalanuvchi topilmaganda ro'yxatdan o'tishga tezkor o'tish
function switchToRegisterWithUser(username) {
    switchAuthTab('register');
    const regUser = document.getElementById('reg_user');
    const regPass = document.getElementById('reg_pass');
    if (regUser) {
        regUser.value = username;
    }
    if (regPass) {
        regPass.focus();
    }
}

function getQueryRedirect() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('redirect') || '/';
    } catch (_) {
        return '/';
    }
}

// 1. Tizimga Kirish
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
            errorEl.innerHTML = "<span>⚠️ Iltimos, login va parolni kiriting!</span>";
            errorEl.style.display = 'block';
        }
        return;
    }

    if (btn) {
        btn.disabled = true;
        btn.innerHTML = 'Tekshirilmoqda... ⏳';
    }
    if (errorEl) errorEl.style.display = 'none';

    fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: username,
            password: password,
            redirect: getQueryRedirect()
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            try {
                localStorage.setItem('zooventure_saved_username', username);
            } catch (_) {}

            const role = data.role || (data.user && data.user.role) || 'user';
            const isAdmin = role === 'admin';
            const msg = isAdmin ? "ADMINISTRATOR TASDIQLANDI... XUSH KELIBSIZ!" : 'IDENTIFIKATSIYA TASDIQLANDI... XUSH KELIBSIZ!';
            playEntranceTransition(msg, data.redirect || (isAdmin ? '/admin' : '/'));
        } else {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = 'Tizimga Kirish 🔓';
            }
            if (errorEl) {
                if (data.user_exists === false) {
                    const safeUser = username.replace(/"/g, '&quot;').replace(/'/g, "\'");
                    errorEl.innerHTML = `
                        <div style="margin-bottom: 0.6rem;">${data.message || 'Bunday login topilmadi!'}</div>
                        <button type="button" onclick="switchToRegisterWithUser('${safeUser}')" style="width: 100%; padding: 0.6rem 0.8rem; background: #10b981; border: none; border-radius: 7px; color: #ffffff; font-weight: 700; cursor: pointer; font-size: 0.85rem; box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4); display: flex; align-items: center; justify-content: center; gap: 0.4rem;">
                            <span>✨</span> <span>'${username}' nomi bilan ro'yxatdan o'tish</span>
                        </button>
                    `;
                } else {
                    errorEl.innerHTML = `<span>⚠️ ${data.message || "Login yoki parol noto'g'ri!"}</span>`;
                }
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
            errorEl.innerHTML = "<span>⚠️ Server bilan aloqa xatosi! Qaytadan urinib ko'ring.</span>";
            errorEl.style.display = 'block';
        }
    });
}

// 2. Ro'yxatdan O'tish
function submitRegister(e) {
    if (e) e.preventDefault();

    const userInput = document.getElementById('reg_user');
    const nameInput = document.getElementById('reg_name');
    const passInput = document.getElementById('reg_pass');
    const passConfirmInput = document.getElementById('reg_pass_confirm');
    const errorEl = document.getElementById('registerError');
    const successEl = document.getElementById('registerSuccess');
    const btn = document.getElementById('btnRegisterSubmit');

    const username = userInput ? userInput.value.trim() : '';
    const name = nameInput ? nameInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';
    const passwordConfirm = passConfirmInput ? passConfirmInput.value.trim() : '';

    if (errorEl) errorEl.style.display = 'none';
    if (successEl) successEl.style.display = 'none';

    if (!username) {
        showRegisterError("Iltimos, login kiriting!");
        if (userInput) userInput.focus();
        return;
    }

    if (username.length < 3) {
        showRegisterError("Login kamida 3 ta belgidan iborat bo'lishi kerak!");
        if (userInput) userInput.focus();
        return;
    }

    if (!password) {
        showRegisterError("Iltimos, parol kiriting!");
        if (passInput) passInput.focus();
        return;
    }

    if (password.length < 4) {
        showRegisterError("Parol kamida 4 ta belgidan iborat bo'lishi kerak!");
        if (passInput) passInput.focus();
        return;
    }

    if (password !== passwordConfirm) {
        showRegisterError("Kiritilgan parollar bir-biriga mos kelmadi!");
        if (passConfirmInput) passConfirmInput.focus();
        return;
    }

    if (btn) {
        btn.disabled = true;
        btn.innerHTML = "Ro'yxatdan o'tilmoqda... ⏳";
    }

    fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: username,
            password: password,
            name: name,
            redirect: getQueryRedirect()
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            try {
                localStorage.setItem('zooventure_saved_username', username);
            } catch (_) {}

            if (successEl) {
                successEl.innerHTML = `✅ <strong>Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!</strong> Tizimga kirilmoqda...`;
                successEl.style.display = 'block';
            }

            playEntranceTransition("RO'YXATDAN O'TISH MUVAFFAQIYATLI YAKUNLANDI... XUSH KELIBSIZ!", data.redirect || getQueryRedirect() || '/');
        } else {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = "Ro'yxatdan o'tish ✨";
            }
            showRegisterError(data.message || "Ro'yxatdan o'tishda xatolik yuz berdi.");
        }
    })
    .catch(() => {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = "Ro'yxatdan o'tish ✨";
        }
        showRegisterError("Server bilan aloqa xatosi! Internet aloqasini tekshiring.");
    });
}

function showRegisterError(msg) {
    const errorEl = document.getElementById('registerError');
    if (errorEl) {
        errorEl.innerHTML = `<span>⚠️ ${msg}</span>`;
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

// 3. Mehmon (Demo) kirish
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

// Kirish o'tish animatsiyasi
function playEntranceTransition(customText, customRedirect) {
    const overlay = document.getElementById('aiSplashOverlay');
    if (overlay) {
        overlay.classList.remove('hidden');
        const status = overlay.querySelector('.ai-status-text');
        if (status) status.innerText = customText || 'AI IDENTIFIKATSIYA TASDIQLANDI... XUSH KELIBSIZ!';
    }
    setTimeout(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const redirect = urlParams.get('redirect') || customRedirect || '/';
        window.location.href = redirect;
    }, 1200);
}

// Sahifa yuklanganda: saqlangan loginni avtomatik to'ldirish
document.addEventListener('DOMContentLoaded', function() {
    let savedUser = '';
    try {
        savedUser = localStorage.getItem('zooventure_saved_username') || '';
    } catch (_) {}

    const userInput = document.getElementById('login_user');
    const passInput = document.getElementById('login_pass');

    if (savedUser && userInput) {
        userInput.value = savedUser;
        if (passInput) passInput.focus();
    } else if (userInput) {
        userInput.focus();
    }

    try {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('mode') === 'register' || window.location.hash === '#register') {
            switchAuthTab('register');
        }
    } catch (_) {}
});

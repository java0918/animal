/**
 * ANIMORE — Admin Panel Boshqaruvi
 */

async function uploadFile(fileInputId, fileType, targetUrlInputId, previewImgId = null) {
    const input = document.getElementById(fileInputId);
    if (!input || !input.files || input.files.length === 0) return;

    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_type', fileType);

    const statusEl = document.getElementById(fileInputId + '_status');
    if (statusEl) statusEl.innerText = 'Yuklanmoqda... ⏳';

    try {
        const resp = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        const data = await resp.json();
        if (data.url) {
            document.getElementById(targetUrlInputId).value = data.url;
            if (statusEl) statusEl.innerText = 'Yuklandi! ✅';
            if (previewImgId) {
                const img = document.getElementById(previewImgId);
                if (img) img.src = data.url;
            }
        } else {
            if (statusEl) statusEl.innerText = 'Xatolik yuz berdi ❌';
        }
    } catch (e) {
        if (statusEl) statusEl.innerText = 'Yuklashda xato ❌';
    }
}

async function saveAnimal(event) {
    event.preventDefault();
    const form = document.getElementById('animalForm');
    const animalId = document.getElementById('animalId').value;

    const data = {
        name_uz: document.getElementById('name_uz').value,
        name_latin: document.getElementById('name_latin').value,
        name_en: document.getElementById('name_en').value,
        category: document.getElementById('category').value,
        class_name: document.getElementById('class_name').value,
        diet: document.getElementById('diet').value,
        habitat: document.getElementById('habitat').value,
        lifespan: document.getElementById('lifespan').value,
        speed: document.getElementById('speed').value,
        weight: document.getElementById('weight').value,
        description: document.getElementById('description').value,
        uz_red_book_status: document.getElementById('uz_red_book_status').value,
        uz_red_book_desc: document.getElementById('uz_red_book_desc').value,
        iucn_status: document.getElementById('iucn_status').value,
        iucn_desc: document.getElementById('iucn_desc').value,
        similar_species: document.getElementById('similar_species').value,
        differences: document.getElementById('differences').value,
        sound_file: document.getElementById('sound_file').value,
        sound_description: document.getElementById('sound_description').value,
        sound_type: document.getElementById('sound_type').value,
        image_url: document.getElementById('image_url').value,
        gallery_images: [],
        fun_facts: document.getElementById('fun_facts').value.split('\n').filter(s => s.trim().length > 0)
    };

    const isEdit = animalId && animalId.trim().length > 0;
    const url = isEdit ? `/api/animals/${animalId}` : '/api/animals';
    const method = isEdit ? 'PUT' : 'POST';

    const saveBtn = document.getElementById('saveAnimalBtn');
    saveBtn.innerText = 'Saqlanmoqda...';

    try {
        const resp = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const res = await resp.json();
        if (res.success) {
            alert(isEdit ? 'Hayvon ma\'lumotlari yangilandi!' : 'Yangi hayvon muvaffaqiyatli qo\'shildi!');
            window.location.reload();
        } else {
            alert('Saqlashda xatolik: ' + (res.message || 'Xato'));
            saveBtn.innerText = 'Saqlash';
        }
    } catch (e) {
        alert('Server xatosi');
        saveBtn.innerText = 'Saqlash';
    }
}

async function deleteAnimal(id, name) {
    if (!confirm(`Haqiqatan ham "${name}" hayvonini o'chirmoqchimisiz?`)) return;

    try {
        const resp = await fetch(`/api/animals/${id}`, { method: 'DELETE' });
        const res = await resp.json();
        if (res.success) {
            window.location.reload();
        } else {
            alert('O\'chirishda xatolik');
        }
    } catch (e) {
        alert('Server bilan bog\'lanishda xato');
    }
}

async function editAnimalById(id) {
    try {
        const resp = await fetch(`/api/animals/${id}`);
        if (!resp.ok) {
            alert('Hayvon ma\'lumotlarini yuklab bo\'lmadi');
            return;
        }
        const animal = await resp.json();
        editAnimalData(animal);
    } catch (e) {
        alert('Server bilan bog\'lanishda xatolik yuz berdi');
    }
}

function editAnimalData(animal) {
    document.getElementById('formTitle').innerText = 'Hayvonni tahrirlash';
    document.getElementById('animalId').value = animal.id;
    document.getElementById('name_uz').value = animal.name_uz || '';
    document.getElementById('name_latin').value = animal.name_latin || '';
    document.getElementById('name_en').value = animal.name_en || '';
    document.getElementById('category').value = animal.category || 'Sutemizuvchilar';
    document.getElementById('class_name').value = animal.class_name || 'Mammalia';
    document.getElementById('diet').value = animal.diet || '';
    document.getElementById('habitat').value = animal.habitat || '';
    document.getElementById('lifespan').value = animal.lifespan || '';
    document.getElementById('speed').value = animal.speed || '';
    document.getElementById('weight').value = animal.weight || '';
    document.getElementById('description').value = animal.description || '';
    document.getElementById('uz_red_book_status').value = animal.uz_red_book_status || 'Kiritilmagan';
    document.getElementById('uz_red_book_desc').value = animal.uz_red_book_desc || '';
    document.getElementById('iucn_status').value = animal.iucn_status || 'LC';
    document.getElementById('iucn_desc').value = animal.iucn_desc || '';
    document.getElementById('similar_species').value = animal.similar_species || '';
    document.getElementById('differences').value = animal.differences || '';
    document.getElementById('sound_file').value = animal.sound_file || '';
    document.getElementById('sound_description').value = animal.sound_description || '';
    document.getElementById('sound_type').value = animal.sound_type || 'roar';
    document.getElementById('image_url').value = animal.image_url || '';
    
    const preview = document.getElementById('imagePreview');
    if (preview && animal.image_url) preview.src = animal.image_url;

    if (Array.isArray(animal.fun_facts)) {
        document.getElementById('fun_facts').value = animal.fun_facts.join('\n');
    }

    switchAdminTab('editAnimalTab');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetAnimalForm() {
    document.getElementById('animalForm').reset();
    document.getElementById('animalId').value = '';
    document.getElementById('formTitle').innerText = 'Yangi hayvon qo\'shish';
    const preview = document.getElementById('imagePreview');
    if (preview) preview.src = 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?auto=format&fit=crop&w=400&q=80';
}

async function saveSettings(event) {
    event.preventDefault();
    const google_client_id = document.getElementById('setting_google_client_id').value;
    const gemini_api_key = document.getElementById('setting_gemini_api_key').value;

    try {
        const resp = await fetch('/api/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                google_client_id: google_client_id,
                gemini_api_key: gemini_api_key
            })
        });
        const res = await resp.json();
        if (res.success) {
            alert('Sozlamalar saqlandi!');
        }
    } catch (e) {
        alert('Saqlashda xatolik');
    }
}

function switchAdminTab(tabId) {
    document.querySelectorAll('.admin-section').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.admin-tab').forEach(el => el.classList.remove('active'));

    const target = document.getElementById(tabId);
    if (target) target.style.display = 'block';

    const tabBtn = document.querySelector(`[data-tab="${tabId}"]`);
    if (tabBtn) tabBtn.classList.add('active');
}

async function pushToGitHub() {
    const token = document.getElementById('github_token_input').value.trim();
    const statusEl = document.getElementById('githubPushStatus');
    const btn = document.getElementById('btnGithubPush');

    if (!token) {
        alert('Iltimos, GitHub tokeningizni kiriting!');
        return;
    }

    btn.disabled = true;
    btn.innerHTML = 'Yuklanmoqda... ⏳';
    statusEl.innerText = '';

    try {
        const resp = await fetch('/api/github/push', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: token })
        });
        const res = await resp.json();
        if (res.success) {
            statusEl.innerText = 'Yuklandi! ✅ https://github.com/java0918/animal';
            statusEl.style.color = '#4ade80';
            alert('Muvaffaqiyatli! Barcha kodlar GitHub ga push qilindi!');
        } else {
            statusEl.innerText = 'Xatolik: ' + res.message;
            statusEl.style.color = '#f87171';
            alert('GitHub xatosi: ' + res.message);
        }
    } catch (e) {
        statusEl.innerText = 'Server xatosi';
        statusEl.style.color = '#f87171';
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span>🚀</span> Kodlarni GitHub ga Yuklash (Push)';
    }
}


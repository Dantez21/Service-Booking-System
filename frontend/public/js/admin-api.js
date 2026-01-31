const API_BASE_URL = "http://127.0.0.1:8000/api";
const ADMIN_TOKEN = "supersecretkey";

let isEditing = false;
let currentEditId = null;

document.addEventListener('DOMContentLoaded', () => {
    const projectList = document.getElementById('admin-project-list');
    if (projectList) fetchAdminProjects();

    const projectForm = document.getElementById('add-project-form');
    if (projectForm) projectForm.addEventListener('submit', handleProjectSubmit);

    // Modal Toggles
    const modal = document.getElementById('project-modal');
    document.getElementById('open-project-modal')?.addEventListener('click', () => {
        isEditing = false;
        projectForm.reset();
        document.getElementById('modal-title').innerText = "Add New Project";
        document.getElementById('prj-file').required = true;
        modal.classList.add('active');
    });
    document.getElementById('close-project-modal')?.addEventListener('click', () => modal.classList.remove('active'));
});

// --- FETCH PROJECTS ---
async function fetchAdminProjects() {
    try {
        const response = await fetch(`${API_BASE_URL}/projects/`);
        const projects = await response.json();
        const tableBody = document.getElementById('admin-project-list');
        
        tableBody.innerHTML = projects.map(proj => `
            <tr>
                <td><strong>${proj.title}</strong></td>
                <td><span class="mng-badge">${proj.category}</span></td>
                <td>
                    <button class="mng-btn-blue" onclick='prepareEdit(${JSON.stringify(proj)})'>Edit</button>
                    <button class="mng-btn-delete" onclick="deleteProject(${proj.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (err) { console.error("Fetch failed", err); }
}

// --- SUBMIT (CREATE/UPDATE) ---
async function handleProjectSubmit(e) {
    e.preventDefault();
    const submitBtn = document.getElementById('prj-submit-btn');
    submitBtn.disabled = true;
    submitBtn.innerText = "Processing...";

    const formData = new FormData();
    formData.append('title', document.getElementById('prj-title').value);
    formData.append('description', document.getElementById('prj-desc').value);
    formData.append('category', document.getElementById('prj-category').value);
    formData.append('github_link', document.getElementById('prj-github').value || "");
    formData.append('live_demo', document.getElementById('prj-demo').value || "");
    
    const fileInput = document.getElementById('prj-file');
    if (fileInput.files[0]) {
        formData.append('file', fileInput.files[0]);
    }

    const url = isEditing ? `${API_BASE_URL}/projects/${currentEditId}` : `${API_BASE_URL}/projects/`;
    const method = isEditing ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'x-admin-token': ADMIN_TOKEN },
            body: formData
        });

        if (response.ok) {
            alert("Success!");
            location.reload();
        } else {
            const errorData = await response.json();
            alert("Error: " + JSON.stringify(errorData.detail));
        }
    } catch (err) {
        alert("Server connection failed");
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = "Save Project";
    }
}

// --- PREPARE EDIT ---
window.prepareEdit = (proj) => {
    isEditing = true;
    currentEditId = proj.id;
    document.getElementById('prj-title').value = proj.title;
    document.getElementById('prj-desc').value = proj.description;
    document.getElementById('prj-category').value = proj.category;
    document.getElementById('prj-github').value = proj.github_link || "";
    document.getElementById('prj-demo').value = proj.live_demo || "";
    document.getElementById('prj-file').required = false;
    document.getElementById('modal-title').innerText = "Edit Project";
    document.getElementById('project-modal').classList.add('active');
};

// --- DELETE ---
async function deleteProject(id) {
    if (!confirm("Delete project?")) return;
    try {
        const response = await fetch(`${API_BASE_URL}/projects/${id}`, {
            method: 'DELETE',
            headers: { 'x-admin-token': ADMIN_TOKEN }
        });
        if (response.ok) fetchAdminProjects();
    } catch (err) { alert("Delete failed"); }
}
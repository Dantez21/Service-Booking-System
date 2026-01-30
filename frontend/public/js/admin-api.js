const API_BASE_URL = "http://127.0.0.1:8000/api";
// const API_BASE_URL = "http://192.168.0.61:8000/api";
// const API_BASE_URL = "https://daniel-portfolio-backend.onrender.com/api";

// This must match the ADMIN_SECRET_TOKEN in your backend
// const ADMIN_TOKEN = "your_super_secret_token_123"; 
const ADMIN_TOKEN = "supersecretkey";

let isEditing = false;
let currentEditId = null;

document.addEventListener('DOMContentLoaded', () => {
    fetchAdminProjects();
    const projectForm = document.getElementById('add-project-form');
    if (projectForm) {
        projectForm.addEventListener('submit', handleFormSubmit);
    }
});

// --- UI HELPERS ---
function toggleModal(show) {
    const modal = document.getElementById('project-modal');
    if (modal) modal.style.display = show ? 'flex' : 'none';
}

function closeModal() {
    isEditing = false;
    currentEditId = null;
    document.getElementById('add-project-form').reset();
    document.querySelector('.modal-content h3').innerText = "Add New Project";
    document.getElementById('prj-file').required = true;
    toggleModal(false);
}

// --- API CALLS ---

async function fetchAdminProjects() {
    try {
        const response = await fetch(`${API_BASE_URL}/projects/`);
        const projects = await response.json();
        const tableBody = document.getElementById('admin-project-list');
        if (!tableBody) return;

        tableBody.innerHTML = ''; 
        projects.forEach(project => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${project.title}</td>
                <td><span class="mng-badge mng-bg-blue">${project.category}</span></td>
                <td>
                    <div class="mng-actions">
                        <button class="mng-btn-blue edit-btn">Edit</button>
                        <button class="mng-btn-delete" onclick="deleteProject(${project.id})">Delete</button>
                    </div>
                </td>
            `;
            row.querySelector('.edit-btn').onclick = () => openEditModal(project);
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Fetch error:", error);
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('title', document.getElementById('prj-title').value);
    formData.append('description', document.getElementById('prj-desc').value);
    formData.append('category', document.getElementById('prj-category').value);
    formData.append('github_link', document.getElementById('prj-github').value);
    
    const fileInput = document.getElementById('prj-file');
    if (fileInput.files[0]) {
        formData.append('file', fileInput.files[0]);
    }

    const url = isEditing ? `${API_BASE_URL}/projects/${currentEditId}` : `${API_BASE_URL}/projects/`;
    const method = isEditing ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'x-admin-token': ADMIN_TOKEN // AUTHENTICATION HEADER
            },
            body: formData
        });

        if (response.ok) {
            alert("Success!");
            closeModal();
            fetchAdminProjects();
        } else {
            const err = await response.json();
            alert("Error: " + err.detail);
        }
    } catch (error) {
        alert("Connection failed.");
    }
}

function openEditModal(project) {
    isEditing = true;
    currentEditId = project.id;
    document.getElementById('prj-title').value = project.title;
    document.getElementById('prj-desc').value = project.description;
    document.getElementById('prj-category').value = project.category;
    document.getElementById('prj-github').value = project.github_link || '';
    document.getElementById('prj-file').required = false;
    document.querySelector('.modal-content h3').innerText = "Edit Project";
    toggleModal(true);
}

async function deleteProject(id) {
    if (!confirm("Delete this project?")) return;

    try {
        const response = await fetch(`${API_BASE_URL}/projects/${id}`, {
            method: 'DELETE',
            headers: {
                'x-admin-token': ADMIN_TOKEN // AUTHENTICATION HEADER
            }
        });

        if (response.ok) {
            fetchAdminProjects();
        } else {
            alert("Delete failed. Unauthorized.");
        }
    } catch (error) {
        alert("Server error.");
    }
}
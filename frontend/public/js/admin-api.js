// --- CONFIGURATION ---
const SERVER_URL = "http://127.0.0.1:8000"; 
const API_BASE_URL = `${SERVER_URL}/api`;

// Global state for modal control
window.isEditing = false;
window.currentEditId = null;

document.addEventListener('DOMContentLoaded', () => {
    console.log("🚀 Admin API Script Loaded");
    fetchAdminProjects();

    const projectForm = document.getElementById('add-project-form');
    if (projectForm) {
        projectForm.addEventListener('submit', handleProjectSubmit);
    }
});

// --- FETCH & RENDER PROJECTS ---
async function fetchAdminProjects() {
    try {
        // Fetch from the API (Note: ensure your FastAPI routes match this URL)
        const response = await fetch(`${API_BASE_URL}/projects/`);
        if (!response.ok) throw new Error("Failed to fetch projects");
        
        const projects = await response.json();
        const tableBody = document.getElementById('admin-project-list');
        
        if (!tableBody) return;

        tableBody.innerHTML = projects.map(proj => {
            // FIX: If image_url is just a filename, point it to /uploads/
            // If it's already a full path like 'static/uploads/file.jpg', prepend SERVER_URL
            let imgPath = proj.image_url;
            if (!imgPath.startsWith('http')) {
                // Adjust this based on how your backend saves the path
                // If backend saves 'uploads/image.jpg', this results in http://127.0.0.1:8000/uploads/image.jpg
                imgPath = imgPath.startsWith('/') ? `${SERVER_URL}${imgPath}` : `${SERVER_URL}/${imgPath}`;
            }

            return `
                <tr>
                    <td>
                        <img src="${imgPath}" class="admin-project-thumb" 
                             onerror="this.src='https://via.placeholder.com/50'" 
                             style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">
                    </td>
                    <td><strong>${proj.title}</strong></td>
                    <td><span class="mng-badge">${proj.category}</span></td>
                    <td>
                        <button class="mng-btn-blue" onclick='prepareEdit(${JSON.stringify(proj)})'>
                            <i class="fa-solid fa-pen"></i> Edit
                        </button>
                        <button class="mng-btn-delete" onclick="deleteProject(${proj.id})">
                            <i class="fa-solid fa-trash"></i> Delete
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (err) {
        console.error("❌ Fetch failed:", err);
    }
}

// --- SUBMIT (CREATE / UPDATE) ---
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
    
    const fileInput = document.getElementById('prj-file');
    if (fileInput.files[0]) {
        formData.append('file', fileInput.files[0]);
    } else if (!window.isEditing) {
        alert("Please select an image file!");
        resetBtn(submitBtn);
        return;
    }

    const url = window.isEditing 
        ? `${API_BASE_URL}/projects/${window.currentEditId}/` 
        : `${API_BASE_URL}/projects/`;
    
    const method = window.isEditing ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            body: formData 
        });

        if (response.ok) {
            alert("Success!");
            location.reload(); 
        } else {
            const errData = await response.json();
            alert("Error: " + (errData.detail || "Action failed"));
        }
    } catch (err) {
        console.error("Network Error:", err);
        alert("Server connection failed. Is the backend running at " + SERVER_URL + "?");
    } finally {
        resetBtn(submitBtn);
    }
}

function resetBtn(btn) {
    btn.disabled = false;
    btn.innerText = "Upload & Save";
}

// --- PREPARE EDIT (Global) ---
window.prepareEdit = (proj) => {
    window.isEditing = true;
    window.currentEditId = proj.id;
    
    document.getElementById('prj-title').value = proj.title;
    document.getElementById('prj-desc').value = proj.description;
    document.getElementById('prj-category').value = proj.category;
    document.getElementById('prj-github').value = proj.github_link || "";
    
    const modalTitle = document.getElementById('modal-title-text');
    if (modalTitle) modalTitle.innerText = "Edit Project";
    
    document.getElementById('prj-file').required = false;
    const helpText = document.getElementById('file-help-text');
    if (helpText) helpText.innerText = "Leave blank to keep current image";
    
    if (typeof toggleModal === 'function') toggleModal(true);
};

// --- DELETE PROJECT ---
window.deleteProject = async (id) => {
    if (!confirm("Are you sure you want to delete this project?")) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/projects/${id}/`, {
            method: 'DELETE'
        });
        if (response.ok) {
            fetchAdminProjects();
        } else {
            alert("Delete failed");
        }
    } catch (err) {
        console.error("Delete error:", err);
    }
};
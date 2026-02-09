/**
 * ADMIN SERVICES LOGIC
 * Handles: Load Services, Add New Service, Delete Service
 */

const SERVICES_API = `${API_BASE_URL}/services/`;
const ADMIN_TOKEN = "supersecretkey";  // Optional if you have auth header

// ------------------------------
// Load all services
// ------------------------------
async function loadAdminServices() {
    try {
        const response = await fetch(SERVICES_API, {
            headers: { "x-admin-token": ADMIN_TOKEN }
        });

        if (!response.ok) throw new Error("Failed to load services");

        const services = await response.json();
        const tableBody = document.getElementById('admin-services-list');

        if (!tableBody) return;

        tableBody.innerHTML = services.map(s => `
            <tr>
                <td><i class="fa-solid ${s.icon_class}"></i></td>
                <td><strong>${s.title}</strong></td>
                <td>${s.description ? s.description.substring(0, 50) : ''}...</td>
                <td>
                    <button onclick="deleteService(${s.id})" class="mng-btn-delete">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');

    } catch (err) {
        console.error("Load Services Error:", err);
        alert("Unable to load services. Check backend.");
    }
}

// ------------------------------
// Handle "Add Service" form submission
// ------------------------------
async function handleServiceSubmit(e) {
    e.preventDefault();

    const title = document.getElementById('srv-title').value.trim();
    const icon_class = document.getElementById('srv-icon').value.trim();
    const description = document.getElementById('srv-desc').value.trim();

    if (!title || !icon_class) {
        alert("Title and Icon are required!");
        return;
    }

    const serviceData = { title, icon_class, description };

    try {
        const response = await fetch(SERVICES_API, {
            method: 'POST',
            headers: { 
                "Content-Type": "application/json",
                "x-admin-token": ADMIN_TOKEN
            },
            body: JSON.stringify(serviceData)
        });

        if (response.ok) {
            document.getElementById('service-modal').classList.remove('active');
            document.getElementById('add-service-form').reset();
            await loadAdminServices();
            alert("Service added successfully!");
        } else {
            const err = await response.json();
            alert("Error: " + (err.detail || JSON.stringify(err)));
        }

    } catch (err) {
        console.error("Add Service Error:", err);
        alert("Failed to add service. Check server logs.");
    }
}

// ------------------------------
// Delete a service
// ------------------------------
async function deleteService(id) {
    if (!confirm("Delete this service?")) return;

    try {
        const response = await fetch(`${SERVICES_API}${id}/`, {  // ✅ Added trailing slash
            method: 'DELETE',
            headers: { "x-admin-token": ADMIN_TOKEN }
        });

        if (response.ok) {
            await loadAdminServices();
            alert("Service deleted successfully!");
        } else {
            const err = await response.json();
            alert("Error deleting service: " + (err.detail || JSON.stringify(err)));
        }

    } catch (err) {
        console.error("Delete Service Error:", err);
        alert("Failed to delete service. Check server logs.");
    }
}

// ------------------------------
// Initialize Service Form & Table
// ------------------------------
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('admin-services-list')) loadAdminServices();

    const serviceForm = document.getElementById('add-service-form');
    if (serviceForm) serviceForm.addEventListener('submit', handleServiceSubmit);
});

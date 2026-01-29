// const API_BASE_URL = "http://127.0.0.1:8000/api";
const API_BASE_URL = "https://daniel-portfolio-backend.onrender.com/api";

let allProjects = []; 
let currentCategory = 'all';

document.addEventListener('DOMContentLoaded', () => {
    fetchProjects();
});

async function fetchProjects() {
    const grid = document.getElementById('projects-grid');
    try {
        const response = await fetch(`${API_BASE_URL}/projects/`);
        if (!response.ok) throw new Error("Failed to fetch");
        
        allProjects = await response.json();
        renderProjects(allProjects);
    } catch (error) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding:50px;">
            <i class="fa-solid fa-circle-exclamation fa-3x" style="color:#ff4d4d;"></i>
            <p>Unable to load projects.</p>
        </div>`;
    }
}

// Unified function to handle both Search and Filter
function applyFilters() {
    const searchTerm = document.getElementById('prj-search-input').value.toLowerCase();
    
    const filtered = allProjects.filter(project => {
        const matchesCategory = (currentCategory === 'all' || project.category === currentCategory);
        const matchesSearch = project.title.toLowerCase().includes(searchTerm) || 
                              project.description.toLowerCase().includes(searchTerm);
        
        return matchesCategory && matchesSearch;
    });

    renderProjects(filtered);
}

function filterProjects(category, button) {
    currentCategory = category;
    document.querySelectorAll('.prj-pill').forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    applyFilters();
}

function handleSearch() {
    applyFilters();
}

function renderProjects(projectsList) {
    const grid = document.getElementById('projects-grid');
    grid.innerHTML = ''; 

    if (projectsList.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding:50px; color:#888;">
            <i class="fa-solid fa-face-frown fa-2x"></i>
            <p style="margin-top:10px;">No projects match your search.</p>
        </div>`;
        return;
    }

    projectsList.forEach(project => {
        const card = document.createElement('div');
        card.className = 'prj-card';
        card.innerHTML = `
            <div class="prj-image-box">
                <img src="${project.image_url}" alt="${project.title}" onerror="this.src='https://via.placeholder.com/400x250'">
                <div class="prj-overlay">
                    <div class="prj-links">
                        ${project.github_link ? `<a href="${project.github_link}" target="_blank"><i class="fa-brands fa-github"></i></a>` : ''}
                        ${project.live_demo ? `<a href="${project.live_demo}" target="_blank"><i class="fa-solid fa-arrow-up-right-from-square"></i></a>` : ''}
                    </div>
                </div>
            </div>
            <div class="prj-content">
                <div class="prj-tag">${project.category}</div>
                <h3>${project.title}</h3>
                <p>${project.description}</p>
            </div>
        `;
        grid.appendChild(card);
    });
}
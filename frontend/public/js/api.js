/**
 * CENTRAL API LOGIC
 * Handles: Homepage Featured Projects, Full Project Gallery, Search, Filtering, and Detail Modals
 */

// --- CONFIGURATION ---
const API_BASE_URL = "http://127.0.0.1:8000/api";
// const API_BASE_URL = "http://192.168.0.61:8000/api"; 
// const API_BASE_URL = "https://daniel-portfolio-backend.onrender.com/api";

let allProjects = []; 
let currentCategory = 'all';
// "Scroll to Top" button that appears only after you've scrolled down
document.addEventListener('DOMContentLoaded', () => {
    const scrollTopBtn = document.getElementById('scroll-top-btn');

    // Show button when user scrolls down 400px
    window.addEventListener('scroll', () => {
        if (window.scrollY > 400) {
            scrollTopBtn.classList.add('show');
        } else {
            scrollTopBtn.classList.remove('show');
        }
    });

    // Smooth scroll to top on click
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const projectsGrid = document.getElementById('projects-grid');          // Project Page ID
    const featuredGrid = document.getElementById('featured-projects-container'); // Homepage ID

    if (projectsGrid) {
        initProjectPage();
    } else if (featuredGrid) {
        initHomePage();
    }
});

// menu closing, the icon reset, and the smooth scroll all at once.
document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.idx-nav-links a');

    // Function to close the menu
    const closeMenu = () => {
        navMenu.classList.remove('active');
        // Reset the icon back to the hamburger bars
        const icon = navToggle.querySelector('i');
        icon.classList.replace('fa-xmark', 'fa-bars');
    };

    // 1. Toggle Menu logic
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        const icon = navToggle.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-xmark');
    });

    // 2. Link Click logic (Close menu + Smooth Scroll)
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');

            // Only run custom scroll if it's an internal link (starts with #)
            if (targetId.startsWith('#')) {
                e.preventDefault();
                
                // STEP A: Immediately close the mobile menu
                closeMenu();

                // STEP B: The Cinematic Smooth Scroll
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    // Short delay to let the menu finish closing visually
                    setTimeout(() => {
                        const offsetPosition = targetElement.offsetTop - 80;
                        window.scrollTo({
                            top: offsetPosition,
                            behavior: 'smooth'
                        });
                    }, 300); // 300ms delay for a snappy feel
                }
            }
        });
    });
});
//  About Me Transition Effect
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            // 1. Give the user a tiny visual cue (optional)
            this.style.opacity = "0.5";

            // 2. Wait for your requested delay (e.g., 1 second)
            setTimeout(() => {
                this.style.opacity = "1";
                
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - 80;
                const startPosition = window.pageYOffset;
                const distance = targetPosition - startPosition;
                const duration = 1000; // How long the glide takes (1.5 seconds)
                let start = null;

                // 3. The "Ease-In-Out" Math
                function step(timestamp) {
                    if (!start) start = timestamp;
                    const progress = timestamp - start;
                    
                    // This math formula creates the "settling" effect (acceleration then deceleration)
                    const ease = progress / duration < 0.3 
                        ? 2 * (progress / duration) * (progress / duration) 
                        : -1 + (4 - 2 * (progress / duration)) * (progress / duration);

                    window.scrollTo(0, startPosition + distance * ease);

                    if (progress < duration) {
                        window.requestAnimationFrame(step);
                    }
                }

                window.requestAnimationFrame(step);
            }, 1000); // The delay before the page starts moving
        }
    });
});

const revealSection = () => {
    const aboutContent = document.querySelector('.idx-about-content');
    const windowHeight = window.innerHeight;
    const elementTop = aboutContent.getBoundingClientRect().top;
    const elementVisible = 150;

    if (elementTop < windowHeight - elementVisible) {
        aboutContent.classList.add('reveal');
    }
};

window.addEventListener('scroll', revealSection);
// ==========================================
// 🏠 HOMEPAGE LOGIC (index.html)
// ==========================================

async function initHomePage() {
    const container = document.getElementById('featured-projects-container');
    const bubbleText = document.querySelector('.idx-chat-bubble-inline');

    try {
        const response = await fetch(`${API_BASE_URL}/projects/`);
        if (!response.ok) throw new Error("API Offline");
        
        const projects = await response.json();
        const featured = projects.slice(-3).reverse();

        if (featured.length === 0) {
            container.innerHTML = `<p style="text-align:center; color:#888;">No projects added yet.</p>`;
            return;
        }

        if(bubbleText) bubbleText.innerText = "Here is my latest work!";

        container.innerHTML = featured.map(proj => `
            <div class="idx-project-card">
                <div class="idx-proj-img" style="background-image: url('${proj.image_url || 'https://via.placeholder.com/400x250'}');"></div>
                <div class="idx-proj-content">
                    <h3>${proj.title}</h3>
                    <p class="prj-desc-truncate">${proj.description}</p> 
                    <div class="idx-proj-footer">
                        <button class="idx-btn-proj" onclick='openProjectModal(${JSON.stringify(proj).replace(/'/g, "&apos;")})'>Read More</button>
                        <i class="fa-regular fa-heart idx-heart" onclick="toggleLike(this, ${proj.id})"></i>
                    </div>
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error("Home Init Error:", error);
        container.innerHTML = `<p style="color:red; text-align:center;">Unable to load featured work.</p>`;
    }
}

// ==========================================
// 📂 PROJECTS PAGE LOGIC (projects.html)
// ==========================================

async function initProjectPage() {
    const grid = document.getElementById('projects-grid');
    try {
        const response = await fetch(`${API_BASE_URL}/projects/`);
        if (!response.ok) throw new Error("Failed to fetch");
        
        allProjects = await response.json();
        renderProjects(allProjects);
    } catch (error) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding:50px;"><p>Unable to load gallery.</p></div>`;
    }
}

function renderProjects(projectsList) {
    const grid = document.getElementById('projects-grid');
    if (!grid) return;
    grid.innerHTML = ''; 

    if (projectsList.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding:50px;"><p>No matches found.</p></div>`;
        return;
    }

    projectsList.forEach(project => {
        const card = document.createElement('div');
        card.className = 'prj-card';
        card.innerHTML = `
            <div class="prj-image-box">
                <img src="${project.image_url}" alt="${project.title}" onerror="this.src='https://via.placeholder.com/400x250'">
            </div>
            <div class="prj-content">
                <div class="prj-tag">${project.category || 'General'}</div>
                <h3>${project.title}</h3>
                <p class="prj-desc-truncate">${project.description}</p>
                <button class="read-more-btn" onclick='openProjectModal(${JSON.stringify(project).replace(/'/g, "&apos;")})'>
                    Read More <i class="fa-solid fa-arrow-right-long"></i>
                </button>
            </div>
        `;
        grid.appendChild(card);
    });
}

// ==========================================
// 🖼️ MODAL & INTERACTION LOGIC
// ==========================================

function openProjectModal(project) {
    let modal = document.getElementById('projectModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'projectModal';
        modal.className = 'prj-modal';
        document.body.appendChild(modal);
    }

    modal.innerHTML = `
        <div class="prj-modal-content">
            <span class="close-modal" onclick="closeModal()">&times;</span>
            <img src="${project.image_url || 'https://via.placeholder.com/400x250'}" style="width:100%; border-radius:10px; margin-bottom:20px;">
            <div class="prj-tag" style="display:inline-block; margin-bottom:10px;">${project.category || 'Project'}</div>
            <h2 style="margin-bottom:15px;">${project.title}</h2>
            <div style="line-height:1.8; color:#444; font-size:1.05rem; margin-bottom:25px;">
                ${project.description}
            </div>
            <div class="modal-footer" style="display:flex; gap:15px; border-top:1px solid #eee; padding-top:20px;">
                ${project.live_demo ? `<a href="${project.live_demo}" target="_blank" class="idx-btn-blue" style="text-decoration:none;">Live Demo</a>` : ''}
                ${project.github_link ? `<a href="${project.github_link}" target="_blank" class="idx-btn-green" style="text-decoration:none;">GitHub</a>` : ''}
            </div>
        </div>
    `;
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden'; // Prevent background scroll
}

function closeModal() {
    const modal = document.getElementById('projectModal');
    if (modal) modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function toggleLike(element, projectId) {
    const isLiked = element.classList.contains('fa-solid');
    if (isLiked) {
        element.classList.replace('fa-solid', 'fa-regular');
        element.style.color = '';
    } else {
        element.classList.replace('fa-regular', 'fa-solid');
        element.style.color = '#ff4d4d';
        element.style.transform = 'scale(1.3)';
        setTimeout(() => element.style.transform = 'scale(1)', 200);
    }
}

// Close modal when clicking outside the content box
window.onclick = function(event) {
    const modal = document.getElementById('projectModal');
    if (event.target == modal) closeModal();
}

/** Filter & Search Helpers */
function applyFilters() {
    const searchInput = document.getElementById('prj-search-input');
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : "";
    const filtered = allProjects.filter(p => {
        const matchesCat = (currentCategory === 'all' || p.category === currentCategory);
        const matchesSearch = p.title.toLowerCase().includes(searchTerm) || p.description.toLowerCase().includes(searchTerm);
        return matchesCat && matchesSearch;
    });
    renderProjects(filtered);
}

function filterProjects(category, button) {
    currentCategory = category;
    document.querySelectorAll('.prj-pill').forEach(btn => btn.classList.remove('active'));
    if(button) button.classList.add('active');
    applyFilters();
}

function handleSearch() { applyFilters(); }
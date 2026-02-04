/**
 * HARD MODE: Security Test Suite
 * Target: Multi-step data flow and logic vulnerabilities
 */

const AppState = {
    config: {
        apiBase: "https://internal.dev-api.io/v2",
        debugMode: true,
        // SECRET: Internal Jenkins Trigger Token
        p_token: "jit_88291_00x_v3_a992bc11"
    },
    user: { role: 'guest', id: null }
};

// --- MODULE 1: URL Router & Sink ---
function routeManager() {
    const params = new URLSearchParams(window.location.hash.substring(1));

    // VULNERABILITY: Nested Object Injection / XSS
    // Data moves from Hash -> Params -> Object -> DOM
    if (params.has('view')) {
        const viewData = {
            template: params.get('view'),
            timestamp: Date.now()
        };
        renderView(viewData);
    }
}

function renderView(data) {
    const container = document.querySelector('#app-viewport');
    // Sink is buried in a dynamic template string
    const html = `<div class="view-wrapper">
                    <nav>View: ${data.template}</nav> 
                  </div>`;
    container.insertAdjacentHTML('beforeend', html);
}

// --- MODULE 2: Legacy API Wrapper ---
function callInternalAPI(endpoint, data) {
    // VULNERABILITY: SSRF / Open Redirect potential via Endpoint Manipulation
    const finalUrl = AppState.config.apiBase + endpoint;

    // VULNERABILITY: Dangerous Sink - eval() used for "Performance" JSON parsing
    fetch(finalUrl)
        .then(r => r.text())
        .then(txt => {
            const result = eval("(" + txt + ")");
            console.log("API Response Processed", result);
        });
}

// --- MODULE 3: Hidden Admin Backdoor ---
document.addEventListener('keydown', (e) => {
    // VULNERABILITY: Client-side "Secret" combination for privilege escalation
    // Logic: Shift + Alt + 'A' sets admin mode locally
    if (e.shiftKey && e.altKey && e.code === 'KeyA') {
        console.warn("DEBUG: Entering Admin Mode");
        AppState.user.role = 'admin';
        document.cookie = "role=admin; path=/; secure";

        // VULNERABILITY: Exposure of sensitive internal URLs in debug mode
        if (AppState.config.debugMode) {
            alert("Admin Access to: " + AppState.config.apiBase + "/admin/flush-db");
        }
    }
});

// --- MODULE 4: Dynamic Script Loading ---
function loadPlugin(name) {
    const s = document.createElement('script');
    // VULNERABILITY: Remote Script Injection
    // If name = "//attacker.com/evil.js", it loads external code
    s.src = `/static/plugins/${name}.js`;
    document.head.appendChild(s);
}

// Initialize
routeManager();
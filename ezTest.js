// test_audit.js - Sample for Security Analysis

// 1. Hardcoded Secrets
const API_KEY = "sk-test-42981-abcdef-99012";
const AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";

// 2. API Endpoints
async function fetchUserData(userId) {
    const url = `https://api.production-env.com/v1/users/${userId}/profile`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${AUTH_TOKEN}`,
            'X-Internal-ID': '9921'
        }
    });
    return response.json();
}

// 3. DOM-based XSS (Source -> Sink)
function updateUsername() {
    const urlParams = new URLSearchParams(window.location.search);
    const username = urlParams.get('name'); // Source: URL Parameter

    // Dangerous Sink: innerHTML
    document.getElementById('display-area').innerHTML = "Welcome, " + username;
}

// 4. Dangerous Code Patterns
function executeDynamicCommand(cmd) {
    // Dangerous: eval() usage
    return eval(cmd);
}

// 5. Logic / Auth Bypass
function checkAdminAccess() {
    const isAdmin = localStorage.getItem('is_admin');

    // Vulnerability: Client-side only check for privilege escalation
    if (isAdmin === "true") {
        document.getElementById('admin-panel').style.display = 'block';
    }
}

// Initialize
updateUsername();
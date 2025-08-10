// Initialize Lucide icons
document.addEventListener("DOMContentLoaded", function() {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Highlight active navigation item
    const navItems = document.querySelectorAll(".nav-item");
    const currentPage = window.location.pathname.split("/").pop();
    
    navItems.forEach((item) => {
        if (item.getAttribute("href") === currentPage) {
            item.classList.add("active");
        }
    });

    // URL Detection Form
    const urlForm = document.getElementById("urlForm");
    if (urlForm) {
        urlForm.addEventListener("submit", function(e) {
            e.preventDefault();
            const urlInput = document.getElementById("urlInput");
            const alertBox = document.getElementById("alert");
            
            // Simulate URL checking
            const isSafe = Math.random() > 0.3; // 70% chance of being safe
            
            alertBox.className = "alert " + (isSafe ? "safe-alert" : "threat-alert");
            alertBox.innerHTML = `
                <i data-lucide="${isSafe ? "check-circle" : "alert-triangle"}"></i>
                <span>This URL is ${isSafe ? "SAFE" : "a POTENTIAL THREAT"}</span>
            `;
            alertBox.classList.remove("hidden");
            
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        });
    }
    
    

     
        
    // Login Form
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", function(e) {
            e.preventDefault();
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const loginButton = document.getElementById("login-button");
            
            loginButton.textContent = "Signing in...";
            loginButton.disabled = true;
            
            fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert("You have been logged in successfully.");
                    window.location.href = "dashboard.html";
                } else {
                    alert(data.error || "Invalid credentials");
                    loginButton.textContent = "Sign in";
                    loginButton.disabled = false;
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error during login.");
                loginButton.textContent = "Sign in";
                loginButton.disabled = false;
            });
        });
    }
    // Signup Form
    const signupForm = document.getElementById("signup-form");
    if (signupForm) {
        signupForm.addEventListener("submit", function(e) {
            e.preventDefault();
            const name = document.getElementById("name").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const signupButton = document.getElementById("signup-button");
            
            signupButton.textContent = "Creating account...";
            signupButton.disabled = true;

            fetch("http://127.0.0.1:5000/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, email, password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert("Account created successfully! Please login.");
                    window.location.href = "login.html";
                } else {
                    alert(data.error || "Error creating account");
                    signupButton.textContent = "Create account";
                    signupButton.disabled = false;
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error during signup.");
                signupButton.textContent = "Create account";
                signupButton.disabled = false;
            });
        });
    }

    // Profile Form
    const saveProfile = document.getElementById("saveProfile");
    if (saveProfile) {
        saveProfile.addEventListener("click", function() {
            const name = document.getElementById("name").value;
            const email = document.getElementById("email").value;
            
            alert(`Profile updated successfully!\n\nName: ${name}\nEmail: ${email}`);
        });
    }


    // Settings Page
    const saveSettings = document.getElementById("saveSettings");
    if (saveSettings) {
        saveSettings.addEventListener("click", function() {
            const theme = document.querySelector('input[name="theme"]:checked').value;
            const notifications = document.getElementById("notifications").checked;
            
            alert(`Settings saved!\n\nTheme: ${theme}\nNotifications: ${notifications ? "Enabled" : "Disabled"}`);
        });
    }

    /*// URL Checker on Homepage
    const checkURL = function() {
        const urlInput = document.getElementById("urlInput");
        const resultDiv = document.getElementById("result");
        
        if (!urlInput || !resultDiv) return;
        
        const url = urlInput.value.trim();
        if (!url) {
            alert("Please enter a URL to check");
            return;
        }
        
        // Simulate checking
        const isSafe = Math.random() > 0.3; // 70% chance of being safe
        resultDiv.innerHTML = `
            <div class="alert ${isSafe ? "safe-alert" : "threat-alert"}">
                <i data-lucide="${isSafe ? "check-circle" : "alert-triangle"}"></i>
                <span>${url} is ${isSafe ? "SAFE" : "a POTENTIAL THREAT"}</span>
            </div>
        `;
        
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    };
    
    // Make checkURL available globally if needed
    window.checkURL = checkURL;*/



    
});





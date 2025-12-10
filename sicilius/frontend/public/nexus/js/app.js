// DOM Elements
const viewPresence = document.getElementById('view-presentation');
const viewSim = document.getElementById('view-simulation');
const btnPres = document.getElementById('btn-pres');
const btnSim = document.getElementById('btn-sim');

// --- SPLASH SCREEN LOGIC ---
const initApp = () => {
    console.log("🚀 Custom App Init Triggered");

    try {
        generateData(); // From data.js
        console.log("✅ Data generated successfully");

        // Initialize Charts IMMEDIATELY (Don't wait for splash)
        if (window.initCharts) {
            console.log("📊 Initializing Charts (Immediate)...");
            window.initCharts();
        } else {
            console.error("❌ window.initCharts is undefined!");
        }

        // Initialize Animation IMMEDIATELY
        if (window.initRiskNetworkAnimation) {
            console.log("🕸️ Initializing Animation (Immediate)...");
            window.initRiskNetworkAnimation();
        }

    } catch (e) {
        console.error("❌ Error in app initialization:", e);
    }

    console.log("🕒 Timer set for Splash Removal (0.5s)");

    // Simulate initial loading flow (Visuals only)
    setTimeout(() => {
        console.log("✨ Removing Splash Screen (Main Timer)...");
        try {
            const splash = document.getElementById('splash-screen');
            const mainApp = document.getElementById('main-app');

            if (splash) {
                splash.style.opacity = '0';
                splash.style.visibility = 'hidden';
                setTimeout(() => {
                    if (splash) splash.remove();
                    console.log("🗑️ Splash removed from DOM");
                }, 1500);
            }

            if (mainApp) {
                mainApp.style.opacity = '1';
                console.log("✅ Main App Visible");
            }

            // Initialize Charts
            // if (window.initCharts) {
            //     console.log("📊 Initializing Charts...");
            //     window.initCharts();
            // }

            // Initialize Risk Animation
            // if (window.initRiskNetworkAnimation) {
            //     console.log("🕸️ Initializing Animation...");
            //     window.initRiskNetworkAnimation();
            // }
        } catch (err) {
            console.error("🔥 Error inside Splash Timeout:", err);
        }
    }, 500); // Reduced to 0.5s for debugging

    // Safety Backup: Force remove after 5s if still exists
    setTimeout(() => {
        const splash = document.getElementById('splash-screen');
        if (splash) {
            console.warn("⚠️ Safety Backup Triggered: Force removing splash");
            splash.remove();
            const mainApp = document.getElementById('main-app');
            if (mainApp) mainApp.style.opacity = '1';
        }
    }, 5000);
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}

function switchMode(mode) {
    try {
        console.log("Switching mode to:", mode);

        if (mode === 'presentation') {
            // SHOW PRESENTATION
            viewPresence.style.display = 'block';
            viewPresence.style.opacity = '1';

            // HIDE SIMULATION
            viewSim.style.display = 'none';
            viewSim.style.opacity = '0';

            // Button Styles
            btnPres.className = "px-6 py-2 rounded-md text-sm font-medium transition-all duration-300 bg-blue-600 text-white shadow-lg shadow-blue-500/30";
            btnSim.className = "px-6 py-2 rounded-md text-sm font-medium transition-all duration-300 text-slate-400 hover:text-white hover:bg-slate-700";
        } else {
            // HIDE PRESENTATION
            viewPresence.style.display = 'none';

            // SHOW SIMULATION (FORCE)
            viewSim.style.display = 'block';
            viewSim.style.opacity = '1';
            viewSim.style.visibility = 'visible'; // Extra safety

            // Button Styles
            btnSim.className = "px-6 py-2 rounded-md text-sm font-medium transition-all duration-300 bg-blue-600 text-white shadow-lg shadow-blue-500/30";
            btnPres.className = "px-6 py-2 rounded-md text-sm font-medium transition-all duration-300 text-slate-400 hover:text-white hover:bg-slate-700";

            // Initialize Simulation Controls if not already done
            if (window.initSimulation) {
                initSimulation();
            } else {
                console.error("initSimulation function not found!");
            }
        }
    } catch (e) {
        console.error("Error in switchMode:", e);
        alert("Mod değiştirme hatası: " + e.message);
    }
}

// Make globally available
window.switchMode = switchMode;

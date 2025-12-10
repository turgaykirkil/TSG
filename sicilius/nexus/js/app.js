// DOM Elements
const viewPresence = document.getElementById('view-presentation');
const viewSim = document.getElementById('view-simulation');
const btnPres = document.getElementById('btn-pres');
const btnSim = document.getElementById('btn-sim');

// --- SPLASH SCREEN LOGIC ---
document.addEventListener('DOMContentLoaded', () => {
    generateData(); // From data.js

    // Simulate initial loading flow
    setTimeout(() => {
        const splash = document.getElementById('splash-screen');
        const mainApp = document.getElementById('main-app');

        splash.style.opacity = '0';
        splash.style.visibility = 'hidden';

        mainApp.style.opacity = '1';

        // Remove splash after transition to save resources
        setTimeout(() => splash.remove(), 1500);

        // Initialize Charts
        if (window.initCharts) {
            window.initCharts();
        }

        // Initialize Risk Animation
        if (window.initRiskNetworkAnimation) {
            window.initRiskNetworkAnimation();
        }
    }, 2500); // 2.5s splash duration
});

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

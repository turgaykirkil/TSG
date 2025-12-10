function initCharts() {
    // 1. SANKEY (Plotly)
    const sankeyData = {
        type: "sankey",
        orientation: "h",
        node: {
            pad: 20,
            thickness: 20,
            line: { color: "#1e293b", width: 0.5 },
            label: ["Başvuru (1000)", "KKB Skoru < 800", "KKB Uygun", "Sistem Kuralları", "Otomatik Onay", "Uzman İncelemesi", "Onay (Manuel)", "Ret (Sistem/Manuel)"],
            color: ["#3b82f6", "#ef4444", "#3b82f6", "#6366f1", "#10b981", "#f59e0b", "#10b981", "#ef4444"],
            labelfont: { color: "white", size: 12 }
        },
        link: {
            source: [0, 0, 2, 2, 3, 3, 5, 5],
            target: [1, 2, 3, 7, 4, 5, 6, 7],
            value: [300, 700, 600, 100, 450, 150, 100, 50], // Mock flow values
            color: ["rgba(239, 68, 68, 0.4)", "rgba(59, 130, 246, 0.4)", "rgba(99, 102, 241, 0.4)", "rgba(239, 68, 68, 0.2)", "rgba(16, 185, 129, 0.4)", "rgba(245, 158, 11, 0.4)", "rgba(16, 185, 129, 0.4)", "rgba(239, 68, 68, 0.4)"]
        }
    };

    const layoutSankey = {
        font: { size: 10, color: "white" },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        margin: { l: 0, r: 0, t: 20, b: 20 }
    };

    Plotly.newPlot('sankeyChart', [sankeyData], layoutSankey, { responsive: true, displayModeBar: false });

    // 2. BUBBLE (Chart.js) - Segmentation
    const bubbleCtx = document.getElementById('bubbleChart').getContext('2d');
    new Chart(bubbleCtx, {
        type: 'bubble',
        data: {
            datasets: [{
                label: 'VIP Segment',
                data: [{ x: 80, y: 85, r: 15 }, { x: 90, y: 90, r: 20 }],
                backgroundColor: 'rgba(16, 185, 129, 0.6)'
            }, {
                label: 'Riskli / İzleme',
                data: [{ x: 40, y: 30, r: 25 }, { x: 30, y: 40, r: 10 }, { x: 20, y: 20, r: 15 }],
                backgroundColor: 'rgba(239, 68, 68, 0.6)'
            }, {
                label: 'Büyüme Odaklı',
                data: [{ x: 60, y: 70, r: 12 }, { x: 70, y: 60, r: 18 }],
                backgroundColor: 'rgba(59, 130, 246, 0.6)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { title: { display: true, text: 'Kredi Skoru', color: '#94a3b8' }, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } },
                y: { title: { display: true, text: 'Hacim (TL)', color: '#94a3b8' }, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } }
            },
            plugins: { legend: { labels: { color: 'white' } } }
        }
    });

    // 3. RADAR (Chart.js) - Psychometrics
    const radarCtx = document.getElementById('radarChart').getContext('2d');
    new Chart(radarCtx, {
        type: 'radar',
        data: {
            labels: ['Ödeme Niyeti', 'Dürüstlük', 'Öz Kontrol', 'Finansal Okuryazarlık', 'İstikrar'],
            datasets: [{
                label: 'Sistem Ortalaması',
                data: [65, 70, 75, 40, 60],
                borderColor: '#38bdf8',
                backgroundColor: 'rgba(56, 189, 248, 0.2)'
            }, {
                label: 'Riskli Örneklem',
                data: [30, 40, 35, 20, 25],
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.2)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    grid: { color: '#334155' },
                    angleLines: { color: '#334155' },
                    pointLabels: { color: '#cbd5e1', font: { size: 10 } },
                    ticks: { display: false }
                }
            },
            plugins: { legend: { labels: { color: 'white' } } }
        }
    });
}

// --- NEW: Risk Network Contagion Animation ---
function initRiskNetworkAnimation() {
    const canvas = document.getElementById('networkRiskCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // Set canvas size
    const rect = canvas.parentNode.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = 300;

    // Nodes
    const nodes = [];
    const nodeCount = 20; // Increased count slightly

    // Create central risk node
    nodes.push({
        x: canvas.width / 2,
        y: canvas.height / 2,
        vx: 0, vy: 0,
        type: 'risk',
        r: 18,
        infected: true
    });

    // Create other nodes
    for (let i = 1; i < nodeCount; i++) {
        nodes.push({
            x: Math.random() * (canvas.width - 40) + 20,
            y: Math.random() * (canvas.height - 40) + 20,
            vx: (Math.random() - 0.5) * 0.8, // Velocity X
            vy: (Math.random() - 0.5) * 0.8, // Velocity Y
            type: 'clean',
            r: 6 + Math.random() * 6,
            infected: false,
            infectionProgress: 0
        });
    }

    // Edges (connect near nodes)
    // For motion, we'll keep edges dynamic or fixed? Fixed edges with moving nodes looks like elastic.
    // Let's Generate edges once based on proximity, then they stretch.
    const edges = [];
    nodes.forEach((node, i) => {
        nodes.forEach((other, j) => {
            if (i !== j && i < j) { // Avoid duplicates
                const dist = Math.hypot(node.x - other.x, node.y - other.y);
                // Connect if close, OR if it involves the central risk node (to ensure infection spreads)
                if (dist < 150 || node.type === 'risk' || other.type === 'risk') {
                    // Randomly select some edges, enforce risk node connections
                    if (Math.random() > 0.6 || node.type === 'risk' || other.type === 'risk') {
                        edges.push({ source: node, target: other });
                    }
                }
            }
        });
    });

    // Animation Loop
    let time = 0;

    function draw() {
        // Clear
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Update Node Positions (Physics)
        nodes.forEach(node => {
            if (node.type !== 'risk') {
                node.x += node.vx;
                node.y += node.vy;

                // Bounce off walls
                if (node.x < 20 || node.x > canvas.width - 20) node.vx *= -1;
                if (node.y < 20 || node.y > canvas.height - 20) node.vy *= -1;
            } else {
                // Gentle float for central node
                node.x += Math.sin(time * 0.02) * 0.2;
                node.y += Math.cos(time * 0.02) * 0.2;
            }
        });

        // Draw Links
        edges.forEach(edge => {
            ctx.beginPath();
            ctx.moveTo(edge.source.x, edge.source.y);
            ctx.lineTo(edge.target.x, edge.target.y);

            // Logic: If source is infected, chance to infect target
            if (edge.source.infected && !edge.target.infected) {
                // Visualize virus packet
                const speed = 0.03;
                const progress = (time * speed + (edge.source.x + edge.target.y) * 0.01) % 1; // Randomize offset

                // Dash effect for clean links
                ctx.strokeStyle = 'rgba(59, 130, 246, 0.2)';

                // Draw the virus particle
                const px = edge.source.x + (edge.target.x - edge.source.x) * progress;
                const py = edge.source.y + (edge.target.y - edge.source.y) * progress;

                ctx.stroke(); // Draw line first

                ctx.beginPath();
                ctx.arc(px, py, 4, 0, Math.PI * 2);
                ctx.fillStyle = '#ef4444'; // Red virus
                ctx.fill();

                // Infection event visual
                if (progress > 0.98 && Math.random() > 0.95) {
                    edge.target.infected = true;
                }

            } else if (edge.source.infected && edge.target.infected) {
                // Fully infected link
                ctx.strokeStyle = 'rgba(239, 68, 68, 0.4)';
                ctx.lineWidth = 1.5;
                ctx.stroke();
            } else {
                // Clean link
                ctx.strokeStyle = 'rgba(59, 130, 246, 0.1)';
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        });

        // Draw Nodes
        nodes.forEach(node => {
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);

            if (node.type === 'risk') {
                // Central Node Pulsing
                const pulse = 2 + Math.sin(time * 0.1) * 2;
                ctx.shadowColor = '#ef4444';
                ctx.shadowBlur = 10 + pulse;
                ctx.fillStyle = '#ef4444';
            } else if (node.infected) {
                ctx.shadowColor = '#ef4444';
                ctx.shadowBlur = 10;
                ctx.fillStyle = '#ef4444';
            } else {
                ctx.shadowColor = '#3b82f6';
                ctx.shadowBlur = 5;
                ctx.fillStyle = '#3b82f6';
            }

            ctx.fill();
            ctx.shadowBlur = 0;

            // Text Label
            if (node.type === 'risk') {
                ctx.fillStyle = 'white';
                ctx.font = 'bold 10px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('RİSK', node.x, node.y + 4);
            }
        });

        // Reset Infection Simulation Periodically
        time++;
        if (time > 800) {
            nodes.forEach((n, i) => { if (i !== 0) n.infected = false; });
            time = 0;
            // Respawn random positions? No, keep motion smooth.
        }

        requestAnimationFrame(draw);
    }

    draw();
}

window.initCharts = initCharts;
window.initRiskNetworkAnimation = initRiskNetworkAnimation;

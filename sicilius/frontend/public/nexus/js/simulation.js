// --- SIMULATION LOGIC ---

function initSimulation() {
    console.log("Initializing Simulation Module (Deep Data Scenarios)...");
    const drawerSelect = document.getElementById('drawer-select');
    if (drawerSelect && drawerSelect.children.length <= 1) {
        populateDrawerSelect();
    }
}

function populateDrawerSelect() {
    const select = document.getElementById('drawer-select');

    // Clear existing options except default
    while (select.children.length > 1) {
        select.removeChild(select.lastChild);
    }

    // Group companies by Category
    const groupA = document.createElement('optgroup'); groupA.label = "🟢 DÜŞÜK RİSK (Yıldız Müşteriler)";
    const groupB = document.createElement('optgroup'); groupB.label = "🟡 ORTA RİSK (İnceleme Gerektirir)";
    const groupC = document.createElement('optgroup'); groupC.label = "🔴 YÜKSEK RİSK (Dolandırıcılık Şüphesi)";

    MOCK_DB.companies.forEach(company => {
        const option = document.createElement('option');
        option.value = company.id;
        option.textContent = `${company.name} | Sektör: ${company.sector}`;

        if (company.category === 'A') groupA.appendChild(option);
        else if (company.category === 'B') groupB.appendChild(option);
        else groupC.appendChild(option);
    });

    select.appendChild(groupA);
    select.appendChild(groupB);
    select.appendChild(groupC);
}

function simulateUpload() {
    const fileInput = document.getElementById('file-upload');
    if (fileInput.files.length > 0) {
        // Auto-select a random company from 'Manual' group for interesting demo
        const manualCandidates = MOCK_DB.companies.filter(c => c.category === 'B');
        const randomDrawer = manualCandidates[Math.floor(Math.random() * manualCandidates.length)];

        document.getElementById('upload-status').innerHTML = `<span class="text-green-400 font-bold"><i class="fa-solid fa-check mr-2"></i>${fileInput.files[0].name}</span> <span class="text-slate-500 text-xs ml-2">OCR Başarılı (%99.8 Güven)</span>`;
        document.getElementById('drawer-select').value = randomDrawer.id;
        document.getElementById('amount-input').value = Math.floor(Math.random() * 200000) + 150000;
        document.getElementById('issue-date').valueAsDate = new Date();
    }
}

function resetSimulation() {
    document.getElementById('drawer-select').selectedIndex = 0;
    document.getElementById('amount-input').value = '';
    document.getElementById('file-upload').value = '';
    document.getElementById('upload-status').innerHTML = '<span class="text-slate-500">veya dosyayı buraya sürükleyin</span>';

    const overlay = document.getElementById('result-overlay');
    overlay.classList.add('hidden');
    overlay.innerHTML = ''; // Clear content

    ['step-ocr', 'step-enrich', 'step-graph', 'step-decision'].forEach(id => {
        const el = document.getElementById(id);
        el.className = "flex flex-col items-center justify-center space-y-2 p-4 rounded-xl border border-transparent transition-all duration-300"; // Reset classes
        const icon = el.querySelector('i');
        const label = el.querySelector('span');

        el.classList.add('text-slate-600', 'bg-transparent');
        el.classList.remove('text-blue-400', 'bg-blue-900/20', 'border-blue-500/30', 'shadow-lg');

        // Reset specific icons
        if (id === 'step-ocr') icon.className = "fa-solid fa-eye text-2xl mb-2";
        if (id === 'step-enrich') icon.className = "fa-solid fa-database text-2xl mb-2";
        if (id === 'step-graph') icon.className = "fa-solid fa-circle-nodes text-2xl mb-2";
        if (id === 'step-decision') icon.className = "fa-solid fa-gavel text-2xl mb-2";
    });

    // Clear Graph
    Plotly.purge('simGraph');
    document.getElementById('simGraph').innerHTML = '<div class="absolute inset-0 flex items-center justify-center text-slate-600 text-sm flex-col"><i class="fa-solid fa-network-wired text-4xl mb-4 opacity-50"></i><span>Simülasyon Başlatılmadı</span></div>';
}

async function startAnalysis() {
    const drawerId = document.getElementById('drawer-select').value;
    const amountStr = document.getElementById('amount-input').value;

    if (!drawerId || !amountStr) {
        alert("Simülasyon için lütfen bir Firma seçin ve Tutar girin.");
        return;
    }

    const amount = parseInt(amountStr);
    const drawer = MOCK_DB.companies.find(c => c.id === drawerId);
    if (!drawer) return;

    // UI Reset
    const overlay = document.getElementById('result-overlay');
    overlay.classList.add('hidden');
    overlay.innerHTML = '';

    // Clear Graph Area for intermediate visuals
    document.getElementById('simGraph').innerHTML = '';

    // Scroll to pipeline to show animation
    document.getElementById('step-ocr').scrollIntoView({ behavior: 'smooth', block: 'center' });

    // --- STEP 1: OCR ---
    await activateStep('step-ocr', 2000, "Fatura Okunuyor...");
    showIntermediateResult(simulateOCR(drawer, amount));
    await new Promise(r => setTimeout(r, 2500)); // Show for 2.5s

    // --- STEP 2: ENRICHMENT ---
    await activateStep('step-enrich', 2000, "Mali Veriler & İstihbarat Çekiliyor...");
    showIntermediateResult(simulateEnrichment(drawer));
    await new Promise(r => setTimeout(r, 2500)); // Show for 2.5s

    // --- STEP 3: GRAPH ---
    // Clear intermediate result before graph
    document.getElementById('simGraph').innerHTML = '';

    visualizeGraph(drawer);
    await activateStep('step-graph', 2000, "İlişkisel Risk Haritası Çıkarılıyor...");

    // --- STEP 4: DECISION ---
    await activateStep('step-decision', 800, "NEXUS Skor Hesaplanıyor...");

    renderScorecard(drawer, amount);
}

function activateStep(elementId, duration, statusText) {
    return new Promise(resolve => {
        const el = document.getElementById(elementId);
        const icon = el.querySelector('i');

        // Active State
        el.classList.remove('text-slate-600', 'bg-transparent');
        el.classList.add('text-blue-400', 'bg-blue-900/20', 'border-blue-500/50', 'shadow-[0_0_15px_rgba(59,130,246,0.3)]');

        icon.className = "fa-solid fa-circle-notch fa-spin text-2xl mb-2";

        // Optional: Update global status if needed
        // document.getElementById('simulation-status').innerText = statusText;

        setTimeout(() => {
            // Done State
            el.classList.remove('animate-pulse', 'border-blue-500/50');
            el.classList.add('text-green-400', 'bg-green-900/10', 'border-green-500/30');
            icon.className = "fa-solid fa-check-circle text-2xl mb-2";
            resolve();
        }, duration);
    });
}

function visualizeGraph(centerNode) {
    // Determine topology based on risk
    const nodes = [];
    const edges = [];

    // Center Node (Applicant)
    nodes.push({
        id: centerNode.id,
        label: centerNode.name.split(' ')[0],
        color: '#3b82f6', // Blue
        size: 35,
        symbol: 'circle'
    });

    // Generate Neighbors Logic
    let neighborCount = 6;
    let riskFactor = 0; // 0-1

    if (centerNode.category === 'C') { // RISKY
        neighborCount = 8;
        riskFactor = 0.8; // Mostly bad neighbors
    } else if (centerNode.category === 'B') { // MANUAL
        neighborCount = 5;
        riskFactor = 0.3; // Some bad neighbors
    } else { // SAFE
        neighborCount = 7;
        riskFactor = 0.1; // Mostly good
    }

    for (let i = 0; i < neighborCount; i++) {
        const isBad = Math.random() < riskFactor;
        const nodeId = `adj-${i}`;

        nodes.push({
            id: nodeId,
            label: isBad ? 'Riskli' : 'Güvenli',
            color: isBad ? '#ef4444' : '#10b981', // Red or Green
            size: isBad ? 20 : 15, // Bad ones slightly bigger attention
            symbol: isBad ? 'diamond' : 'circle'
        });

        edges.push({ source: centerNode.id, target: nodeId });
    }

    // Creating Plotly traces
    const traceNodes = {
        x: nodes.map((n, i) => i === 0 ? 0 : Math.cos(2 * Math.PI * i / (nodes.length - 1)) * (1 + Math.random() * 0.3)),
        y: nodes.map((n, i) => i === 0 ? 0 : Math.sin(2 * Math.PI * i / (nodes.length - 1)) * (1 + Math.random() * 0.3)),
        mode: 'markers+text',
        text: nodes.map(n => ''), // No text on nodes to keep clean
        hovertext: nodes.map(n => `${n.label} (${n.color === '#ef4444' ? 'Kötü Ödeme' : 'İyi Ödeme'})`),
        hoverinfo: 'text',
        marker: {
            size: nodes.map(n => n.size),
            color: nodes.map(n => n.color),
            line: { color: 'white', width: 2 }
        },
        type: 'scatter'
    };

    // Edges trace (Drawing lines manually for Plotly Scatter)
    const edgeX = [];
    const edgeY = [];
    edges.forEach(edge => {
        const sourceIdx = nodes.findIndex(n => n.id === edge.source);
        const targetIdx = nodes.findIndex(n => n.id === edge.target);

        edgeX.push(traceNodes.x[sourceIdx], traceNodes.x[targetIdx], null);
        edgeY.push(traceNodes.y[sourceIdx], traceNodes.y[targetIdx], null);
    });

    const traceEdges = {
        x: edgeX,
        y: edgeY,
        mode: 'lines',
        line: { color: '#475569', width: 1, shape: 'spline' }, // Slate-600 lines
        hoverinfo: 'none',
        type: 'scatter'
    };

    Plotly.newPlot('simGraph', [traceEdges, traceNodes], {
        showlegend: false,
        xaxis: { showgrid: false, zeroline: false, showticklabels: false, range: [-2, 2] },
        yaxis: { showgrid: false, zeroline: false, showticklabels: false, range: [-2, 2] },
        margin: { l: 0, r: 0, b: 0, t: 0 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    }, { displayModeBar: false, staticPlot: true });
}

// Global helper for interactive calculation
window.updateOffer = function (inputLimit, rate, days) {
    const limit = parseFloat(inputLimit);
    if (isNaN(limit) || limit < 0) return;

    // Factoring Logic: (Principal * Rate * Days) / 36000
    // Net Payment = Principal - Interest (Deduction model)
    const interest = (limit * rate * days) / 36000;
    const netPayment = limit - interest; // Factoring logic: We pay you THIS amount now.

    // Update the DOM
    document.getElementById('calc-interest').innerText = '-' + interest.toLocaleString('tr-TR', { maximumFractionDigits: 0 }) + ' TL';
    document.getElementById('calc-total').innerText = netPayment.toLocaleString('tr-TR', { maximumFractionDigits: 0 }) + ' TL';
};

function renderScorecard(company, amount) {
    const overlay = document.getElementById('result-overlay');
    let decisionData = {};

    // Base Rate Logic (TCMB + Market)
    const baseRate = 45.0;

    // --- SCENARIO STORIES ---
    // Update Limit Logic: Use the exact requested amount, no multiplier.
    if (company.category === 'C') { // HIGH RISK
        decisionData = {
            verdict: "RED",
            titleClass: "text-red-500",
            bgClass: "bg-red-900/20",
            borderClass: "border-red-500/30",
            limit: 0,
            maturity: 0,
            rate: 0,
            spread: 0,
            signals: [
                { title: 'TİCARİ SİCİL', val: 'İFLAS ERTELEME', status: 'critical', desc: 'Resmi gazetede yayınlanmış konkordato ilanı tespit edildi.' },
                { title: 'GRAF AĞI', val: 'DOLANDIRICILIK HALKASI', status: 'critical', desc: 'Firmanın ilişkili olduğu 3 paravan şirket tespit edildi.' },
                { title: 'ÇEK GEÇMİŞİ', val: '%65 YAZILMA', status: 'critical', desc: 'Son 6 ayda ibraz edilen çeklerin çoğu karşılıksız.' }
            ],
            aiReason: "Firma izole değerlendirildiğinde aktif büyüklüğü yeterli görünse de (#MaliVeri), ilişkisel ağ analizinde (#Graph) yüksek riskli bir 'Ponzi' yapısının parçası olduğu tespit edilmiştir. Kesin Red önerilir."
        };
    } else if (company.category === 'B') { // MANUAL / CAUTION
        decisionData = {
            verdict: "MANUEL İNCELEME",
            titleClass: "text-amber-400",
            bgClass: "bg-amber-900/20",
            borderClass: "border-amber-500/30",
            limit: amount, // Exact amount
            maturity: 60, // Restricted tenor
            spread: 7.5, // High risk premium
            rate: baseRate + 7.5,
            signals: [
                { title: 'LİMİT DOLULUK', val: '%85 CİVARI', status: 'warning', desc: 'Mevcut banka limitleri sınıra yakın.' },
                { title: 'NAKİT AKIŞI', val: 'DENGESİZ', status: 'warning', desc: 'Tahsilat vadeleri uzuyor, stok devir hızı düşüyor.' },
                { title: 'SEKTÖR RİSKİ', val: 'DARALMA', status: 'neutral', desc: 'İnşaat sektöründeki genel durgunluk etkileyebilir.' }
            ],
            aiReason: "Firma borcunu ödüyor (#KKB:İyi) ancak nakit akışında ciddi bir sıkışıklık sinyali var (#BankaHareketleri). Talep edilen tutarın tamamı riskli olabilir. Kısmi limit ve ek teminatla ilerlenmesi önerilir."
        };
    } else { // AUTO APPROVE
        decisionData = {
            verdict: "OTOMATİK ONAY",
            titleClass: "text-green-400",
            bgClass: "bg-green-900/20",
            borderClass: "border-green-500/30",
            limit: amount, // Exact amount requested
            maturity: 120, // Long tenor
            spread: 2.4, // Low risk premium
            rate: baseRate + 2.4,
            signals: [
                { title: 'BÜYÜME İVMESİ', val: '%120 YILLIK', status: 'success', desc: 'Ciro ve karlılık sektör ortalamasının çok üzerinde.' },
                { title: 'SADAKAT', val: 'YÜKSEK', status: 'success', desc: 'Tedarikçilerine düzenli ve erken ödeme yapıyor.' },
                { title: 'DİJİTAL AYAK İZİ', val: 'POZİTİF', status: 'success', desc: 'Hakkında olumsuz haber veya dava kaydı yok.' }
            ],
            aiReason: "Mükemmel bir 'Gizli Şampiyon' profili. Bilanço değerleri muhafazakar olsa da, gerçek ticaret hacmi ve ağdaki itibarı çok yüksek (#NetworkScore). Rekabetçi bir oranla kaçırılmaması gereken bir müşteri."
        };
    }

    // New Helper: Calculate Rate from Net Payment (Reverse Logic)
    window.updateRateFromNet = function (netPaymentInput, limit, maturity) {
        const netPayment = parseFloat(netPaymentInput);
        if (isNaN(netPayment)) return;

        // Formula: Net = Limit - Interest
        // Interest = Limit - Net
        const interestAmount = limit - netPayment;

        // Interest = (Limit * Rate * Maturity) / 36000
        // Rate = (Interest * 36000) / (Limit * Maturity)
        let newRate = (interestAmount * 36000) / (limit * maturity);

        // Update Displays
        document.getElementById('calc-interest').textContent = `-${interestAmount.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} TL`;
        document.getElementById('calc-rate-display').textContent = `%${newRate.toFixed(2)}`;

        // Visual feedback
        const rateDisplay = document.getElementById('calc-rate-display');
        rateDisplay.classList.add('text-blue-400');
        setTimeout(() => rateDisplay.classList.remove('text-blue-400'), 300);
    };

    // Helper: Initial Calculation (Forward Logic)
    window.calculateInitialValues = function () {
        const interest = (decisionData.limit * decisionData.rate * decisionData.maturity) / 36000;
        const netPayment = decisionData.limit - interest;

        document.getElementById('calc-interest').textContent = `-${interest.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} TL`;
        document.getElementById('calc-net-input').value = netPayment.toFixed(2); // Set Input Value
    }

    // --- RENDER HTML ---
    const html = `
        <div id="scorecard-container" class="w-full bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden shadow-2xl animate-fade-in-up">
            
            <!-- 1. HEADLINE RESULT (TERM SHEET VIEW) -->
            <div class="px-8 py-5 ${decisionData.bgClass} border-b ${decisionData.borderClass} flex flex-col xl:flex-row justify-between items-start gap-8">
                
                <!-- Verdict Section -->
                <div class="flex-1 min-w-0 w-full xl:w-auto">
                    <div class="flex items-center space-x-3 mb-2">
                        <div class="px-2 py-0.5 rounded bg-slate-950/50 text-slate-400 text-xs font-bold tracking-wider border border-slate-700">NEXUS DECISION ENGINE</div>
                        <div class="text-xs text-slate-500 font-mono">${new Date().toISOString().split('T')[0]}</div>
                    </div>
                    <h2 class="text-4xl md:text-5xl font-black ${decisionData.titleClass} tracking-tight mb-4">${decisionData.verdict}</h2>
                    <p class="text-sm text-slate-300 max-w-xl leading-relaxed opacity-90 border-l-2 border-slate-500/30 pl-4 hidden md:block">
                        "${decisionData.aiReason}"
                    </p>
                </div>

                <!-- Term Sheet Section -->
                ${decisionData.verdict !== 'RED' ? `
                    <div class="bg-slate-950/90 rounded-xl p-5 border border-slate-600/60 w-full xl:w-[420px] shrink-0 backdrop-blur-md shadow-xl">
                        <div class="flex justify-between items-center mb-4 pb-3 border-b border-slate-700">
                            <span class="text-xs font-bold text-slate-400 uppercase">Faktoring Teklifi</span>
                            <span class="text-xs font-mono text-green-400 font-bold"><i class="fa-solid fa-check-circle mr-1"></i>ONAYLANDI</span>
                        </div>
                        
                        <div class="space-y-4">
                            <!-- Check Amount (READ ONLY) -->
                            <div class="bg-slate-900/40 rounded-lg p-3 border-2 border-slate-700">
                                <label class="block text-[10px] uppercase font-bold text-slate-400 mb-1">Çek / Alacak Tutarı (Sabit)</label>
                                <div class="flex items-center justify-between">
                                    <span class="text-2xl font-mono text-white font-bold tracking-tight">${decisionData.limit.toLocaleString('tr-TR')}</span>
                                    <span class="text-slate-400 ml-2 text-lg font-bold">TL</span>
                                </div>
                            </div>

                            <!-- Maturity & Commission -->
                             <div class="grid grid-cols-2 gap-3">
                                <div class="p-2 rounded bg-slate-900/40 border-2 border-slate-700">
                                    <span class="block text-[10px] text-slate-400 mb-1">Vade</span>
                                    <span class="text-sm font-mono text-white font-bold">${decisionData.maturity} GÜN</span>
                                </div>
                                <div class="p-2 rounded bg-slate-900/40 border-2 border-slate-700 text-right">
                                    <span class="block text-[10px] text-slate-400 mb-1">Komisyon</span>
                                    <span class="text-sm font-bold text-green-400">0 TL</span>
                                </div>
                            </div>
                            
                            <!-- Calculations -->
                            <div class="pt-3 border-t border-dashed border-slate-700/50 mt-3 space-y-1">
                                <div class="flex justify-between items-center">
                                    <span class="text-xs text-slate-400">Faiz Oranı (Yıllık / Değişken)</span>
                                    <span id="calc-rate-display" class="text-xs font-mono text-white transition-colors duration-300">%${decisionData.rate.toFixed(2)}</span>
                                </div>
                                <div class="flex justify-between items-center">
                                    <span class="text-xs text-slate-400">Faiz Kesintisi</span>
                                    <span id="calc-interest" class="text-xs font-mono text-red-400">Hesaplanıyor...</span>
                                </div>
                                <div class="bg-green-900/10 p-3 rounded border border-green-500/30 mt-2 focus-within:ring-2 ring-green-500/50 transition-all">
                                    <div class="flex justify-between items-end mb-1">
                                        <div>
                                            <span class="block text-[10px] font-bold text-green-300 opacity-80">NET ELE GEÇECEK (Değiştirilebilir)</span>
                                            <span class="text-[10px] text-green-400">Tutar değiştikçe faiz güncellenir</span>
                                        </div>
                                    </div>
                                    <div class="flex items-center">
                                         <input id="calc-net-input" type="number" 
                                           class="bg-transparent text-2xl font-mono font-bold text-green-400 w-full outline-none tracking-tight border-b border-green-500/30 pb-1"
                                           oninput="window.updateRateFromNet(this.value, ${decisionData.limit}, ${decisionData.maturity})">
                                         <span class="text-green-500 ml-2 font-bold text-sm">TL</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                ` : `
                    <div class="bg-red-950/30 rounded-xl p-8 border border-red-500/30 w-full xl:w-[400px] flex flex-col items-center justify-center text-center">
                        <div class="w-16 h-16 rounded-full bg-red-900/50 text-red-500 flex items-center justify-center text-3xl mb-4 border border-red-500/20">
                            <i class="fa-solid fa-ban"></i>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-2">İşlem Reddedildi</h3>
                        <p class="text-sm text-red-300">Yüksek risk sinyalleri nedeniyle bu talep onaylanmamıştır.</p>
                    </div>
                `}
            </div>

            <!-- 2. DEEP DIVE SIGNALS (Grid) -->
            <div class="bg-slate-950/30 p-8">
                <h3 class="text-xs font-bold text-slate-500 uppercase mb-6 flex items-center tracking-widest">
                    <i class="fa-solid fa-layer-group text-blue-500 mr-2"></i>Risk Sinyal Analizi
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    ${decisionData.signals.map(s => `
                        <div class="group p-4 bg-slate-900 rounded-xl border border-slate-800 hover:border-slate-700 transition relative overflow-hidden">
                             <div class="absolute top-0 right-0 w-16 h-16 bg-gradient-to-br from-white/5 to-transparent rounded-bl-full -mr-8 -mt-8 transition group-hover:from-white/10"></div>
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">${s.title}</span>
                                <i class="fa-solid 
                                    ${s.status === 'critical' ? 'fa-triangle-exclamation text-red-500' :
            s.status === 'warning' ? 'fa-magnifying-glass text-amber-500' :
                'fa-check-circle text-green-500'}"></i>
                            </div>
                            <div class="text-lg font-bold text-white mb-2 font-mono">${s.val}</div>
                            <p class="text-xs text-slate-400 leading-relaxed">${s.desc}</p>
                        </div>
                    `).join('')}
                </div>
            </div>

            <!-- 3. ACTIONS -->
            <div class="bg-slate-950 px-8 py-5 border-t border-slate-800 flex justify-between items-center">
                <button onclick="resetSimulation()" class="text-slate-400 hover:text-white text-sm flex items-center transition group">
                    <i class="fa-solid fa-rotate-left mr-2 group-hover:-rotate-90 transition-transform"></i> Yeni Analiz
                </button>
                ${decisionData.verdict !== 'RED' ? `
                    <button class="bg-blue-600 hover:bg-blue-500 text-white px-8 py-3 rounded-lg text-sm font-bold shadow-lg shadow-blue-500/20 transition flex items-center hover:scale-105 active:scale-95">
                        <i class="fa-solid fa-file-signature mr-2"></i> Resmi Teklifi İndir (PDF)
                    </button>
                ` : ''}
            </div>
        </div>
    `;

    overlay.classList.remove('hidden');
    overlay.innerHTML = html;

    // Trigger initial calculation if approved
    if (decisionData.verdict !== 'RED') {
        window.calculateInitialValues();
    }
}

// --- HELPER FUNCTIONS FOR INTERMEDIATE STEPS ---
function simulateOCR(company, amount) {
    // Generate realistic OCR data based on input
    return {
        title: "BELGE ANALİZİ (OCR)",
        icon: "fa-eye",
        items: [
            { label: "Keşideci VKN", value: company.mernis?.taxId || "1234567890", status: "success" },
            { label: "Çek Tutarı", value: `${amount.toLocaleString('tr-TR')} TL`, status: "success" },
            { label: "Karekod Doğrulama", value: "Geçerli / Eşleşti", status: "success" },
            { label: "İmza Sirküleri", value: company.category === 'C' ? "TUTARSIZLIK TESPİT EDİLDİ (Risk)" : "Eşleşti (%99.9 Oran)", status: company.category === 'C' ? "danger" : "success" }
        ],
        type: 'ocr'
    };
}

function simulateEnrichment(company) {
    let items = [];

    if (company.category === 'A') {
        items = [
            { label: "Ticaret Sicil", value: "FAAL (Kuruluş: 1985)", status: "success" },
            { label: "Bağımsız Denetim", value: "2024 Yılı Olumlu Görüş", status: "success" },
            { label: "Dava/İcra", value: "Kayıt Yok", status: "success" },
            { label: "Sermaye Piyasası", value: "Son Sermaye Artırımı: 2024/Q1", status: "success" }
        ];
    } else if (company.category === 'B') {
        items = [
            { label: "Ticaret Sicil", value: "FAAL (Adres Değişikliği: Yeni)", status: "warning" },
            { label: "SGK / Vergi", value: "Yapılandırılmış Borç Mevcut", status: "warning" },
            { label: "Dava/İcra", value: "1 Adet Ticari Alacak Davası (Davalı)", status: "warning" },
            { label: "Haber Taraması", value: "Sektörde küçülme haberleri", status: "neutral" }
        ];
    } else { // C
        items = [
            { label: "Ticaret Sicil", value: "İFLAS ERTELEME TALEBİ", status: "danger" },
            { label: "Vergi Dairesi", value: "Re'sen Terk Şüphesi", status: "danger" },
            { label: "Mernis Adres", value: "Sanal Ofis / Paylaşımlı", status: "danger" },
            { label: "Yönetim Kurulu", value: "Son 1 yılda 3 kez değişti", status: "danger" }
        ];
    }

    return {
        title: "VERİ ZENGİNLEŞTİRME",
        icon: "fa-database",
        items: items,
        type: 'enrich'
    };
}

function showIntermediateResult(data) {
    const container = document.getElementById('simGraph');

    // Create HTML for the intermediate result card
    const html = `
        <div class="w-full h-full flex flex-col items-center justify-center p-8 animate-fade-in-up">
            <div class="bg-slate-900/90 border border-slate-700/50 rounded-2xl p-6 max-w-lg w-full shadow-2xl backdrop-blur-md">
                <div class="flex items-center space-x-4 mb-6 border-b border-slate-800 pb-4">
                    <div class="w-12 h-12 rounded-lg bg-blue-900/30 text-blue-400 flex items-center justify-center text-xl border border-blue-500/20">
                        <i class="fa-solid ${data.icon}"></i>
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-white">${data.title}</h3>
                        <div class="text-xs text-slate-500 font-mono">LIVE DATA STREAM</div>
                    </div>
                </div>
                
                <div class="space-y-3">
                    ${data.items.map(item => `
                        <div class="flex justify-between items-center p-3 rounded-lg bg-slate-950/50 border border-slate-800/50">
                            <span class="text-sm text-slate-400 font-medium">${item.label}</span>
                            <span class="text-sm font-bold font-mono 
                                ${item.status === 'success' ? 'text-green-400' :
            item.status === 'warning' ? 'text-amber-400' :
                item.status === 'danger' ? 'text-red-500' : 'text-slate-300'}">
                                ${item.value}
                                ${item.status === 'success' ? '<i class="fa-solid fa-check ml-2"></i>' :
            item.status === 'danger' ? '<i class="fa-solid fa-triangle-exclamation ml-2"></i>' : ''}
                            </span>
                        </div>
                    `).join('')}
                </div>

                <div class="mt-6">
                    <div class="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
                        <div class="h-full bg-blue-500 animate-[loading_2.5s_ease-in-out_forwards]"></div>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.innerHTML = html;
}

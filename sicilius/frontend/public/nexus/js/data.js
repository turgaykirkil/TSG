// DOM Elements
const MOCK_DB = {
    companies: [],
    transactions: [],
    graphEdges: []
};

const SECTORS = ['Tekstil', 'İnşaat', 'Otomotiv', 'Lojistik', 'Gıda', 'Teknoloji', 'Perakende', 'Kimya', 'Enerji'];
const CITIES = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Gaziantep', 'Kocaeli', 'Konya', 'Adana'];

const RISK_NOTES = [
    "Piyasa ödemeleri düzenli, çekleri güvenilir.",
    "Son dönemde büyüme odaklı, limit artışı talep edilebilir.",
    "Sektörel daralma nedeniyle dikkatli olunmalı.",
    "Yönetim değişikliği sonrası ödeme alışkanlıkları bozuldu.",
    "Bakiye riski yüksek, ek teminat alınmalı.",
    "Referanslar olumlu, tedarikçi ağı güçlü."
];

function generateData() {
    console.log("Initializing NEXUS deep data universe (Segmented)...");

    // Helper to add company
    const addCompany = (type, index) => {
        const sector = SECTORS[Math.floor(Math.random() * SECTORS.length)];
        let company = {
            id: `N${type}${1000 + index}`, // e.g. NA1000
            name: generateCompanyName(sector),
            sector: sector,
            city: CITIES[Math.floor(Math.random() * CITIES.length)],
            category: type, // 'A' (Approve), 'B' (Manual), 'C' (Reject)

            sicil: {},
            kkb: {},
            mernis: {},
            bank: {},
            intelligence: {},
            erp: {},
            isFraud: false
        };

        if (type === 'A') { // AUTO APPROVE
            company.sicil = { foundationYear: 1980 + Math.floor(Math.random() * 20), capital: 5000000 + Math.random() * 10000000, shareholderStructure: 'Kurumsal/Şeffaf', status: 'Faal' };
            company.kkb = { score: 1600 + Math.floor(Math.random() * 300), checkIndex: 1200 + Math.floor(Math.random() * 400), limitRatio: Math.floor(Math.random() * 40), pastDue: 0 };
            company.mernis = { taxId: Math.floor(1000000000 + Math.random() * 9000000000), addressRisk: 'Düşük', blacklistedRelation: false };
            company.bank = { factoringLimit: 10000000, currentRisk: 1000000, blockedChecks: 0 };
            company.intelligence = { visitDate: 'Güncel', sentiment: 'Olumlu', note: 'Sektörün lider firmalarından.' };
            company.erp = { stockTurnover: '30 Gün', annualTurnover: '>100M TL' };
        } else if (type === 'B') { // MANUAL / GREY
            company.sicil = { foundationYear: 2018 + Math.floor(Math.random() * 5), capital: 500000 + Math.random() * 500000, shareholderStructure: 'Aile Şirketi', status: 'Faal' };
            company.kkb = { score: 1100 + Math.floor(Math.random() * 300), checkIndex: 800 + Math.floor(Math.random() * 300), limitRatio: 75 + Math.floor(Math.random() * 15), pastDue: Math.floor(Math.random() * 10000) };
            company.mernis = { taxId: Math.floor(1000000000 + Math.random() * 9000000000), addressRisk: 'Orta', blacklistedRelation: false };
            company.bank = { factoringLimit: 2000000, currentRisk: 1500000, blockedChecks: 0 };
            company.intelligence = { visitDate: '6 Ay Önce', sentiment: 'Nötr', note: 'Hızlı büyüyor, nakit akışı sıkışık olabilir.' };
            company.erp = { stockTurnover: '90 Gün', annualTurnover: '20-50M TL' };
        } else { // AUTO REJECT
            company.sicil = { foundationYear: 2023 + Math.floor(Math.random() * 2), capital: 100000, shareholderStructure: 'Karmaşık/Belirsiz', status: 'Faal' };
            company.kkb = { score: 500 + Math.floor(Math.random() * 400), checkIndex: 200 + Math.floor(Math.random() * 400), limitRatio: 95 + Math.floor(Math.random() * 5), pastDue: 100000 + Math.floor(Math.random() * 500000) };
            company.mernis = { taxId: Math.floor(1000000000 + Math.random() * 9000000000), addressRisk: 'Yüksek (Sanal Ofis)', blacklistedRelation: true };
            company.bank = { factoringLimit: 0, currentRisk: 500000, blockedChecks: Math.floor(Math.random() * 5) + 1 };
            company.intelligence = { visitDate: 'Yapılmadı', sentiment: 'Olumsuz', note: 'Piyasada olumsuz söylentiler mevcut.' };
            company.erp = { stockTurnover: 'Veri Yok', annualTurnover: 'Bilinmiyor' };
            company.isFraud = Math.random() < 0.5; // High fraud chance
        }

        MOCK_DB.companies.push(company);
    };

    // Generate 10 of each type
    for (let i = 0; i < 10; i++) addCompany('A', i);
    for (let i = 0; i < 10; i++) addCompany('B', i);
    for (let i = 0; i < 10; i++) addCompany('C', i);

    // 2. Generate Transactions & Graph (Generic structure for viz)
    const statuses = ['Ödendi', 'Gecikmeli', 'Yazıldı'];
    for (let i = 0; i < 200; i++) {
        const drawer = MOCK_DB.companies[Math.floor(Math.random() * MOCK_DB.companies.length)];
        const payee = MOCK_DB.companies[Math.floor(Math.random() * MOCK_DB.companies.length)];
        if (drawer.id === payee.id) continue;

        MOCK_DB.graphEdges.push({ source: drawer.id, target: payee.id });
    }
}

function generateCompanyName(sector) {
    const prefixes = ['Anadolu', 'Mega', 'Asya', 'Avrasya', 'Yıldız', 'Global', 'Meta', 'Hız', 'Birlik', 'Ege', 'Marmara', 'Karadeniz'];
    const suffixes = ['Dış Ticaret', 'Sanayi', 'Pazarlama', 'Lojistik', 'İmalat', 'Yatırım'];
    return `${prefixes[Math.floor(Math.random() * prefixes.length)]} ${suffixes[Math.floor(Math.random() * suffixes.length)]} ${sector} A.Ş.`;
}

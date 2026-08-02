const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());

// DB'yi oku
const dbPath = path.join(__dirname, 'db.json');

const readDatabase = () => {
  try {
    const rawData = fs.readFileSync(dbPath);
    return JSON.parse(rawData);
  } catch (error) {
    console.error('Database read error:', error);
    return { users: [], customers: [], tasks: [] };
  }
};

// Login endpoint
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;

  console.log('Login request:', { email, password }); // Debug log

  const db = readDatabase();
  const user = db.users.find(u => 
    u.email === email && 
    u.password === password
  );

  console.log('Found user:', user); // Debug log

  if (user) {
    res.json({
      success: true,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role
      }
    });
  } else {
    res.status(401).json({
      success: false,
      message: 'Invalid credentials'
    });
  }
});

// Diğer endpoint'ler için json-server benzeri basit router
const createRouter = (resource) => {
  return {
    get: (id, filters = {}) => {
      try {
        const db = readDatabase();
        
        // Eğer resource db'de yoksa boş array döndür
        if (!db[resource]) {
          console.warn(`Resource '${resource}' not found in database`);
          return [];
        }

        let items = id ? [db[resource].find(item => item.id === id)] : db[resource];
        
        // null değerleri filtrele
        items = items.filter(Boolean);
        
        // Filtreleme mantığı
        if (!id && Object.keys(filters).length > 0) {
          items = items.filter(item => {
            return Object.entries(filters).every(([key, value]) => {
              if (!item || value === undefined) return false;
              
              // salesRepId kontrolü
              if (key === 'salesRepId') {
                const itemSalesRepId = item.salesRepId ? item.salesRepId.toString() : null;
                const filterSalesRepId = value ? value.toString() : null;
                return itemSalesRepId === filterSalesRepId;
              }
              
              // Diğer filtreler için genel kontrol
              if (typeof item[key] === 'string' && typeof value === 'string') {
                return item[key].toLowerCase() === value.toLowerCase();
              } else {
                return item[key] === value;
              }
            });
          });
        }
        
        return id ? (items[0] || null) : items;
      } catch (error) {
        console.error('Router Error:', error);
        return [];
      }
    },
    post: (data) => {
      try {
        const db = readDatabase();
        // Eğer resource db'de yoksa oluştur
        if (!db[resource]) {
          db[resource] = [];
        }
        const newItem = { ...data, id: Date.now().toString() };
        db[resource].push(newItem);
        fs.writeFileSync(dbPath, JSON.stringify(db, null, 2));
        return newItem;
      } catch (error) {
        console.error('Router Post Error:', error);
        throw error;
      }
    }
  };
};

// Dinamik route'lar
['customers', 'tasks', 'sales'].forEach(resource => {
  app.get(`/api/${resource}`, (req, res) => {
    try {
      const router = createRouter(resource);
      const userRole = req.headers['x-user-role']?.toLowerCase();
      const userId = req.headers['x-user-id'];

      // Admin ve supervisor için tüm verileri döndür
      if (userRole === 'admin' || userRole === 'supervisor') {
        const items = router.get();
        return res.json(items);
      }

      // Diğer roller için filtreleme yap
      const items = router.get(null, { salesRepId: userId });
      res.json(items);

    } catch (error) {
      console.error('Route Error:', error);
      res.status(500).json({ error: error.message });
    }
  });

  app.get(`/api/${resource}/:id`, (req, res) => {
    try {
      const router = createRouter(resource);
      const item = router.get(req.params.id);
      item ? res.json(item) : res.status(404).json({ message: 'Not found' });
    } catch (error) {
      console.error('Route Error:', error);
      res.status(500).json({ error: error.message });
    }
  });

  app.post(`/api/${resource}`, (req, res) => {
    try {
      const router = createRouter(resource);
      const newItem = router.post(req.body);
      res.status(201).json(newItem);
    } catch (error) {
      console.error('Route Error:', error);
      res.status(500).json({ error: error.message });
    }
  });
});

const PORT = 3000;
const HOST = '0.0.0.0';
app.listen(PORT, HOST, () => {
  console.log(`Server running on http://${HOST}:${PORT}`);
});

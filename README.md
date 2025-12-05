# 🏢 TSG Platform - Monorepo

Enterprise-grade company intelligence platform for analyzing Turkish Trade Registry Gazette data.

## 📦 Repository Structure

```
TSG_Platform/
├── 📁 sicilius/           # Main Sicilius platform
│   ├── backend/           # FastAPI backend service
│   ├── frontend/          # Next.js frontend application
│   ├── ocr_app/           # Swift OCR companion app (macOS/iOS)
│   └── docker-compose.yml # Docker orchestration
│
├── 📄 build_backend.sh    # Backend build script
└── 📄 README.md           # This file
```

## 🚀 Quick Start

```bash
cd sicilius
docker-compose up -d --build
```

See [sicilius/README.md](sicilius/README.md) for detailed documentation.

## 📚 Documentation

- **Main Platform:** [sicilius/README.md](sicilius/README.md)
- **Backend API:** [sicilius/backend/README.md](sicilius/backend/README.md)
- **Frontend App:** [sicilius/frontend/README.md](sicilius/frontend/README.md)
- **OCR App:** [sicilius/ocr_app/README.md](sicilius/ocr_app/README.md)

## 🛠 Tech Stack Overview

| Component | Technologies |
|-----------|-------------|
| **Backend** | FastAPI, PostgreSQL, MinIO, Redis |
| **Frontend** | Next.js 14, TailwindCSS, TypeScript |
| **OCR** | Swift, Tesseract, GPT-4 |
| **DevOps** | Docker, Caddy, GitHub Actions |

## 📋 Prerequisites

- Docker 20.10+ & Docker Compose
- Python 3.10+ (for local dev)
- Node.js 18+ (for local dev)
- PostgreSQL 13+ (via Docker)

## 🌟 Key Features

- ✅ **Automated OCR** - PDF processing with Tesseract & GPT-4
- 🔍 **Smart Search** - Fuzzy search with relationship mapping
- 📊 **Analytics** - Company trends and visualizations
- 🗺️ **Geospatial** - Location-based search with PostGIS
- 🔐 **RBAC** - Role-based access control
- 📧 **Email Integration** - Cloudflare Email Routing

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Made with ❤️ by Sicilius Team**

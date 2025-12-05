# ⚛️ Frontend

Next.js web application for Sicilius platform.

## 🛠 Tech Stack

- Next.js 14 - React framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Radix UI - Component library
- TanStack Query - Data fetching
- Leaflet - Maps

## 📂 Structure

```
frontend/
├── src/
│   ├── app/          # Next.js App Router
│   ├── components/   # Shared components
│   ├── contexts/     # React contexts
│   └── hooks/        # Custom hooks
├── public/           # Static assets
└── package.json
```

## 🚀 Quick Start

```bash
# Install dependencies
yarn install

# Setup environment
cp .env.local.example .env.local

# Start dev server
yarn dev
```

Visit http://localhost:3000

## 🐳 Docker

```bash
docker build -t sicilius-frontend .
docker run -p 3000:3000 sicilius-frontend
```

## 🔑 Environment

```env
NEXT_PUBLIC_API_URL=http://localhost:5001/api/v1
```

## 📱 Pages

- `/` - Home page
- `/login` - Authentication
- `/dashboard` - Main dashboard
- `/admin` - Admin panel

## 🎨 Design System

Built with shadcn/ui components and Tailwind CSS.

## 📦 Build

```bash
# Production build
yarn build

# Start production server
yarn start
```

## 📝 License

MIT License

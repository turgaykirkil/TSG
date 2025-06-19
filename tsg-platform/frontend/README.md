# TSG Platform Frontend

Modern, performant, and accessible frontend for the TSG Platform, built with Next.js, TypeScript, and Tailwind CSS.

## 🚀 Features

- ⚡ Next.js 13+ with App Router
- 🎨 Tailwind CSS with dark mode support
- 🔒 Built-in authentication with NextAuth.js
- 🛣️ File-based routing
- 🎯 TypeScript for type safety
- 🎨 Radix UI components for accessible UI
- 🔄 TanStack Query for data fetching and caching
- 📱 Fully responsive design

## 📦 Prerequisites

- Node.js 18.0.0 or later
- Yarn 1.22.0 or later

## 🛠️ Installation

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/tsg-platform.git
   cd tsg-platform/frontend
   ```

2. Install dependencies:

   ```bash
   yarn install
   ```

3. Create a `.env.local` file in the root directory and add the required environment variables (see `.env.example` for reference)

## 🚀 Getting Started

### Development

To start the development server:

```bash
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Building for Production

To create a production build:

```bash
yarn build
```

To start the production server:

```bash
yarn start
```

## 🧭 Project Structure

```
frontend/
├── app/                    # App Router pages and layouts
│   ├── (app)/              # Authenticated routes
│   │   └── dashboard/      # Dashboard pages
│   ├── (public)/           # Public routes
│   │   ├── login/          # Login page
│   │   └── register/       # Register page
│   └── api/                # API routes
├── components/             # Reusable UI components
│   ├── ui/                 # Shadcn/ui components
│   └── layout/             # Layout components
├── lib/                    # Utility functions and configurations
├── public/                 # Static assets
├── styles/                 # Global styles and Tailwind configuration
└── types/                  # TypeScript type definitions
```

## 🛠️ Technologies Used

- [Next.js](https://nextjs.org/) - React framework
- [TypeScript](https://www.typescriptlang.org/) - Type checking
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [NextAuth.js](https://next-auth.js.org/) - Authentication
- [TanStack Query](https://tanstack.com/query) - Data fetching and caching
- [Radix UI](https://www.radix-ui.com/) - Accessible UI primitives
- [Lucide Icons](https://lucide.dev/) - Icons

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

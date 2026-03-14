# ShadowAlpha - Web Frontend

This repository contains the frontend application for ShadowAlpha, a quantitative peer-to-peer markets and digital tontine platform.

## Tech Stack
- Next.js 14 (App Router)
- React 19
- Tailwind CSS 4
- TypeScript 5
- Zustand (State Management)
- TanStack React Query (Data Fetching)
- Framer Motion (Animations)
- Recharts (Data Visualization)
- Lucide React (Icons)
- React Hook Form + Zod (Form Validation)

## Getting Started

### Prerequisites
- Node.js 18.x or later
- npm or pnpm

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Application

Start the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint checks
- `npm run format` - Format code with Prettier
- `npm run check-types` - Run TypeScript type checking without emitting files

## Project Structure
- `/src/app` - Next.js App Router pages and layouts
- `/src/components` - Reusable UI components
  - `/ui` - Base UI elements (buttons, inputs, cards)
  - `/charts` - Recharts visualizations
  - `/layout` - Shared layout elements (headers, sidebars)
- `/src/hooks` - Custom React hooks
- `/src/lib` - Utility functions, constants, and API clients
- `/src/stores` - Zustand state management stores
- `/src/types` - TypeScript interfaces and types

## Brand Guidelines
The project adheres to the strict ShadowAlpha brand guide, utilizing:
- **Colors**: Deep surface tones with sharp Gold (`#C9A84C`) accents
- **Typography**: Syne (Display), DM Sans/Inter (Body), JetBrains Mono (Data)
- **Effects**: Glassmorphism (`glass-panel`), inner shadows, and dynamic gradient borders.

## Day 1-2 Execution Checklist
- [x] Initialized Next.js 14 with TypeScript and Tailwind
- [x] Configured absolute paths and strict typing
- [x] Implemented Brand Colors, Typography, and utility classes
- [x] State Management setup (Zustand + local storage persistence)
- [x] API Client structure setup
- [x] Reusable component library (Button, Card, Input, Badge, Modal)
- [x] Dashboard UI with Tontine & Exchange Mockups
- [x] Authentication logic stub (Login, Signup, KYC)
- [x] React Query integration
- [x] CI/CD Pre-flight setup (Lint, Format, Check-types)

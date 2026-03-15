export const APP_CONFIG = {
  name: "Shadow Alpha",
  description: "AI-Powered Quantitative Trading Intelligence",
  currency: "XAF", // Default to CEMAC regional currency
  languages: ["fr", "en"],
  defaultLang: "fr",
};

export const ROUTES = {
  HOME: "/",
  LOGIN: "/login",
  SIGNUP: "/signup",
  KYC: "/kyc",
  DASHBOARD: "/dashboard",
  EXCHANGE: "/exchange",
  TONTINE: "/tontine",
  HISTORY: "/history",
  VAULT: "/vault",
  SHIELD: "/shield",
  SUBSCRIPTION: "/subscription",
  PROFILE: "/profile",
  SETTINGS: "/settings",
  DOCS: "/docs",
};

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: "/auth/login",
    REGISTER: "/auth/register",
    ME: "/auth/me",
  },
  PORTFOLIO: {
    SUMMARY: "/portfolio/summary",
    HISTORY: "/portfolio/history",
  },
  EXCHANGE: {
    ORDERBOOK: "/exchange/orderbook",
    INSTANT_CASHOUT_QUOTE: "/exchange/instant-cashout/quote",
    INSTANT_CASHOUT_EXECUTE: "/exchange/instant-cashout/execute",
  },
  TONTINE: {
    MY_GROUPS: "/tontine/groups/my",
  },
  VAULT: {
    DEPOSIT: "/vault/deposit",
    WITHDRAW: "/vault/withdraw",
    PERFORMANCE: "/vault/performance",
  },
  SHIELD: {
    QUOTE: "/shield/quote",
    ACTIVATE: "/shield/activate",
    CLAIM: "/shield/claim",
    CONTRACTS: "/shield/my",
  },
  SUBSCRIPTION: {
    PLANS: "/subscription/plans",
    CURRENT: "/subscription/current",
    UPGRADE: "/subscription/upgrade",
    CANCEL: "/subscription/cancel",
  },
  GRATITUDE: {
    TIP: "/gratitude/tip",
    SUPPORTERS: "/gratitude/supporters",
  },
  CREDIT: {
    SCORE: "/credit/score",
  },
};

export const COPY = {
  fr: {
    nav: {
      dashboard: "Tableau de bord",
      exchange: "Échange",
      tontine: "Tontine",
      history: "Historique",
      vault: "Coffre-Fort",
      shield: "Bouclier",
      subscription: "Abonnement",
      profile: "Profil",
      settings: "Paramètres",
      docs: "API Docs",
    },
    common: {
      loading: "Chargement...",
      error: "Une erreur est survenue.",
      save: "Enregistrer",
      cancel: "Annuler",
    },
  },
  en: {
    nav: {
      dashboard: "Dashboard",
      exchange: "Exchange",
      tontine: "Tontine",
      history: "History",
      vault: "Vault",
      shield: "Shield",
      subscription: "Plans",
      profile: "Profile",
      settings: "Settings",
      docs: "API Docs",
    },
    common: {
      loading: "Loading...",
      error: "An error occurred.",
      save: "Save",
      cancel: "Cancel",
    },
  },
};

export interface Position {
  id: string;
  assetSymbol: string;
  assetName: string;
  direction: "LONG" | "SHORT";
  entryPrice: number;
  currentPrice: number;
  quantity: number;
  leverage: number;
  unrealizedPnl: number;
  unrealizedPnlPct: number;
  status: "ACTIVE" | "CLOSED" | "PENDING";
  createdAt: string;
  expiresAt?: string;
}

export interface P2POrder {
  id: string;
  sellerId: string;
  sellerKycVerified: boolean;
  position: Position;
  askPrice: number;
  negotiable: boolean;
  minBuyerKycLevel: 0 | 1 | 2 | 3;
  listingDate: string;
  expiresAt: string;
  status: "OPEN" | "FILLED" | "CANCELLED";
}

export interface Portfolio {
  totalValue: number;
  availableMargin: number;
  usedMargin: number;
  unrealizedPnl: number;
  positions: Position[];
  dailyPnl: number;
  dailyPnlPct: number;
}

export interface Trade {
  id: string;
  orderId: string;
  buyerId: string;
  sellerId: string;
  position: Position;
  executedPrice: number;
  executedAt: string;
  fees: number;
}

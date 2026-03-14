export interface TontineMember {
  id: string;
  name: string;
  avatarUrl?: string;
  phone?: string;
  kycLevel: 0 | 1 | 2 | 3;
  contributionStatus: "PENDING" | "PAID" | "LATE";
  joinedAt: string;
}

export interface TontineGroup {
  id: string;
  name: string;
  currency: "XAF" | "EUR" | "USD";
  contributionAmount: number;
  frequency: "WEEKLY" | "BIWEEKLY" | "MONTHLY";
  members: TontineMember[];
  currentCycle: number;
  totalCycles: number;
  nextPayoutDate: string;
  nextBeneficiary: TontineMember;
  status: "ACTIVE" | "FORMING" | "COMPLETED";
  createdAt: string;
}

export interface TontineTransaction {
  id: string;
  groupId: string;
  memberId: string;
  amount: number;
  type: "CONTRIBUTION" | "PAYOUT";
  date: string;
  status: "COMPLETED" | "PENDING" | "FAILED";
}

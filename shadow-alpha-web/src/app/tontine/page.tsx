"use client";

import { useState } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Users, Plus, Trophy, Calendar, Lock } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  useTontineGroups,
  useCreateTontineGroup,
  useTontineContribute,
  useTontineLedger,
} from "@/hooks/use-tontine";
import { formatCurrency } from "@/lib/utils";
import { APP_CONFIG } from "@/lib/constants";

const toNumber = (value: unknown) => {
  if (typeof value === "number") return value;
  if (typeof value === "string") return Number(value);
  return 0;
};

export default function TontinePage() {
  const { data: groupsData, isLoading } = useTontineGroups();
  const createGroup = useCreateTontineGroup();
  const contribute = useTontineContribute();

  const groups = groupsData?.data ?? [];
  const [selectedGroupId, setSelectedGroupId] = useState<string | null>(null);
  const { data: ledgerData } = useTontineLedger(selectedGroupId);
  const ledger = ledgerData?.data ?? [];

  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newGroup, setNewGroup] = useState({
    name: "",
    cycle_type: "monthly",
    target_amount: "50000",
    description: "",
  });

  const [contributeAmount, setContributeAmount] = useState("50000");
  const [contributeGroupId, setContributeGroupId] = useState("");

  const handleCreateGroup = () => {
    if (!newGroup.name) return;
    createGroup.mutate(newGroup, {
      onSuccess: () => {
        setShowCreateForm(false);
        setNewGroup({
          name: "",
          cycle_type: "monthly",
          target_amount: "50000",
          description: "",
        });
      },
    });
  };

  const handleContribute = () => {
    if (!contributeGroupId || !contributeAmount) return;
    contribute.mutate(
      { group_id: contributeGroupId, amount: contributeAmount },
      {
        onSuccess: () => {
          setContributeAmount("50000");
          alert("Contribution successful!");
        },
      },
    );
  };

  return (
    <div className="flex flex-col gap-6 pb-10">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-display font-bold tracking-tight text-white">
            Digital Tontines
          </h1>
          <p className="text-muted-foreground">
            Transparent capital syndication and rotational savings.
          </p>
        </div>
        <Button onClick={() => setShowCreateForm(!showCreateForm)}>
          <Plus className="mr-2 h-4 w-4" /> New Group
        </Button>
      </div>

      {/* Create Group Form */}
      {showCreateForm && (
        <Card className="glass-panel border-gold/20">
          <CardHeader>
            <CardTitle className="text-lg">Create New Tontine Group</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <input
              type="text"
              placeholder="Group Name (e.g. Alpha Syndicate B)"
              value={newGroup.name}
              onChange={(e) =>
                setNewGroup({ ...newGroup, name: e.target.value })
              }
              className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
            />
            <div className="grid grid-cols-2 gap-3">
              <select
                value={newGroup.cycle_type}
                onChange={(e) =>
                  setNewGroup({ ...newGroup, cycle_type: e.target.value })
                }
                className="h-10 rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
              >
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="quarterly">Quarterly</option>
              </select>
              <input
                type="number"
                placeholder="Target Amount"
                value={newGroup.target_amount}
                onChange={(e) =>
                  setNewGroup({ ...newGroup, target_amount: e.target.value })
                }
                className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
              />
            </div>
            <input
              type="text"
              placeholder="Description (optional)"
              value={newGroup.description}
              onChange={(e) =>
                setNewGroup({ ...newGroup, description: e.target.value })
              }
              className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
            />
            <div className="flex gap-2">
              <Button
                onClick={handleCreateGroup}
                disabled={createGroup.isPending}
                className="flex-1"
              >
                {createGroup.isPending ? "Creating..." : "Create Group"}
              </Button>
              <Button
                variant="secondary"
                onClick={() => setShowCreateForm(false)}
                className="flex-1"
              >
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Existing Groups or Empty State */}
        {isLoading ? (
          <Card className="glass-panel lg:col-span-2">
            <CardContent className="p-8 text-center text-muted-foreground">
              Loading your tontine groups...
            </CardContent>
          </Card>
        ) : groups.length === 0 ? (
          <Card className="glass-panel lg:col-span-2">
            <CardContent className="p-8 flex flex-col items-center justify-center gap-4">
              <Users className="h-12 w-12 text-muted-foreground" />
              <h3 className="text-lg font-display font-bold text-white">
                No Tontine Groups Yet
              </h3>
              <p className="text-sm text-muted-foreground text-center max-w-sm">
                Create your first tontine group or join an existing one to start
                building community savings.
              </p>
              <Button onClick={() => setShowCreateForm(true)}>
                <Plus className="mr-2 h-4 w-4" /> Create Your First Group
              </Button>
            </CardContent>
          </Card>
        ) : (
          groups.map((group) => (
            <Card
              key={group.id}
              className={`glass-panel overflow-hidden cursor-pointer transition-all ${
                selectedGroupId === group.id
                  ? "border-gold/40"
                  : "border-border hover:border-gold/20"
              }`}
              onClick={() => setSelectedGroupId(group.id)}
            >
              <div className="h-1 w-full bg-gradient-to-r from-gold/50 to-accent/50" />
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{group.name}</CardTitle>
                  <Badge className="bg-success/20 text-success border-success/30 px-2 rounded-sm text-[10px]">
                    {group.status || "Active"}
                  </Badge>
                </div>
                {group.description && (
                  <CardDescription>{group.description}</CardDescription>
                )}
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-3 w-3 text-muted-foreground" />
                    <span className="text-muted-foreground capitalize">
                      {group.cycle_type}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Lock className="h-3 w-3 text-muted-foreground" />
                    <span className="text-muted-foreground">
                      {formatCurrency(
                        toNumber(group.target_amount),
                        APP_CONFIG.currency as "XAF",
                      )}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Users className="h-3 w-3 text-muted-foreground" />
                    <span className="text-muted-foreground">
                      {group.member_count ?? "—"} members
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Trophy className="h-3 w-3 text-gold" />
                    <span className="text-muted-foreground">
                      Cycle #{group.current_cycle ?? 1}
                    </span>
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-border flex justify-between items-center">
                  <span className="text-xs text-muted-foreground">
                    Total contributed
                  </span>
                  <span className="font-mono text-sm font-bold text-gold">
                    {formatCurrency(
                      toNumber(group.total_contributed),
                      APP_CONFIG.currency as "XAF",
                    )}
                  </span>
                </div>
              </CardContent>
            </Card>
          ))
        )}

        {/* Action Column */}
        <div className="flex flex-col gap-6">
          {/* Contribute Card */}
          <Card className="glass-panel">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm text-muted-foreground">
                Make a Contribution
              </CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
              <select
                value={contributeGroupId}
                onChange={(e) => setContributeGroupId(e.target.value)}
                className="h-10 rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
              >
                <option value="">Select a group...</option>
                {groups.map((g) => (
                  <option key={g.id} value={g.id}>
                    {g.name}
                  </option>
                ))}
              </select>
              <div className="relative">
                <input
                  type="number"
                  placeholder="Amount"
                  value={contributeAmount}
                  onChange={(e) => setContributeAmount(e.target.value)}
                  className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 pl-12 text-sm text-white focus:border-gold focus:outline-none font-mono"
                />
                <div className="absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground font-mono">
                  {APP_CONFIG.currency}
                </div>
              </div>
              <Button
                onClick={handleContribute}
                disabled={
                  !contributeGroupId || !contributeAmount || contribute.isPending
                }
                className="w-full"
              >
                {contribute.isPending ? "Sending..." : "Make Payment"}
              </Button>
            </CardContent>
          </Card>

          {/* Ledger Card */}
          {selectedGroupId && (
            <Card className="glass-panel">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm">Contribution Ledger</CardTitle>
              </CardHeader>
              <CardContent>
                {ledger.length === 0 ? (
                  <p className="text-xs text-muted-foreground text-center py-4">
                    No contributions yet for this group.
                  </p>
                ) : (
                  <div className="space-y-2">
                    {ledger.map((c: { id: string; amount: string; cycle_number: number; created_at: string }) => (
                      <div
                        key={c.id}
                        className="flex items-center justify-between p-2 rounded-lg bg-surface-2 text-sm"
                      >
                        <div>
                          <p className="text-xs text-muted-foreground">
                            Cycle #{c.cycle_number}
                          </p>
                          <p className="text-[10px] text-muted-foreground">
                            {new Date(c.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <span className="font-mono text-white">
                          {formatCurrency(
                            toNumber(c.amount),
                            APP_CONFIG.currency as "XAF",
                          )}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

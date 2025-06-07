import { useState } from "react";
import { api } from "../api";

/* Props type: parent passes a callback so we can trigger a refresh */
interface Props {
  onAdded: () => void;
}

export default function ExpenseForm({ onAdded }: Props) {
  /* ---------- local state for each input field ---------- */
  const [amount, setAmount] = useState("");
  const [date,   setDate]   = useState("");
  const [desc,   setDesc]   = useState("");

  /* ---------- submit handler ---------- */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();                       // stop page reload
    /* POST to /api/expenses */
    await api.post("/expenses", {
      amount: parseFloat(amount),
      date,
      description: desc
      // category omitted → backend auto-categorises
    });
    /* clear the form */
    setAmount("");
    setDate("");
    setDesc("");
    /* tell parent a new row exists → it can re-fetch */
    onAdded();
  };

  /* ---------- JSX (the actual form) ---------- */
  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mt-4">
      <input
        type="number" step="0.01" placeholder="Amount"
        value={amount} onChange={e => setAmount(e.target.value)}
        required className="border px-2 py-1 w-24"
      />
      <input
        type="date"
        value={date} onChange={e => setDate(e.target.value)}
        required className="border px-2 py-1"
      />
      <input
        type="text" placeholder="Description"
        value={desc} onChange={e => setDesc(e.target.value)}
        required className="border flex-1 px-2 py-1"
      />
      <button className="border px-3 py-1 bg-blue-600 text-white">
        Add
      </button>
    </form>
  );
}


import { useEffect, useState } from "react";
import { api } from "../api";

/* ---------- Type for one row coming from the backend ---------- */
type Expense = {
  id: number;
  amount: number;
  date: string;      // ISO string e.g. "2025-06-09"
  desc: string;
  category: string;
  is_anomaly: boolean;   // ← NEW FIELD
};

/* ---------- Main table component ---------- */
export default function ExpenseTable() {
  /* state — holds rows once fetched */
  const [rows, setRows] = useState<Expense[]>([]);

  /* side-effect — run once on mount to fetch data */
  useEffect(() => {
    api.get<Expense[]>("/expenses").then(res => setRows(res.data));
  }, []);

  /* JSX — renders a basic table */
  return (
    <table className="table-auto border-collapse w-full mt-4">
      <thead>
        <tr className="bg-gray-100">
          <th className="px-2 py-1 text-left">Date</th>
          <th className="px-2 py-1 text-left">Description</th>
          <th className="px-2 py-1 text-right">Amount</th>
          <th className="px-2 py-1 text-left">Category</th>
        </tr>
      </thead>
      <tbody>
        {rows.map(r => (
          <tr key={r.id} className="border-b">
            <td className="px-2 py-1">{r.date}</td>
            <td className="px-2 py-1">{r.desc}</td>
            <td className="px-2 py-1 text-right">₹{r.amount.toFixed(2)}</td>
            <td className="px-2 py-1">
              {r.category}
              {/* show warning icon if flagged as anomaly */}
              {r.is_anomaly && <span className="text-red-600 ml-2">⚠️</span>}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

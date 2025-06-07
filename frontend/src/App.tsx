import { useState } from "react";
import ExpenseForm  from "./components/ExpenseForm";
import ExpenseTable from "./components/ExpenseTable";

/**
 * Top-level wrapper.
 *  - Holds a simple "refresh" counter.
 *  - When ExpenseForm finishes POSTing, it increments the counter,
 *    which forces ExpenseTable to remount and re-fetch data.
 */
export default function App() {
  const [refresh, setRefresh] = useState(0);

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: "1rem" }}>
      <h1 style={{ fontSize: 24, fontWeight: 600 }}>Intellex Expense Tracker</h1>

      {/* ExpenseForm notifies us via onAdded */}
      <ExpenseForm onAdded={() => setRefresh(r => r + 1)} />

      {/* key={refresh} => remounts component → triggers new GET /expenses */}
      <ExpenseTable key={refresh} />
    </div>
  );
}

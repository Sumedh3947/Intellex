// src/api.ts
import axios from "axios";

/**
 * Pre-configured Axios instance for all API calls.
 * Usage examples:
 *   api.get("/expenses");
 *   api.post("/expenses", { amount: 12, ... });
 */
export const api = axios.create({
  baseURL: "http://localhost:5001/api",
});


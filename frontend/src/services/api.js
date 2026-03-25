import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 5000,
});

// 🔹 Fetch graph
export const fetchGraph = async () => {
  try {
    const res = await API.get("/graph");

    console.log("GRAPH API:", res.data);

    return {
      nodes: res.data?.nodes || [],
      links: res.data?.links || [],
    };
  } catch (error) {
    console.error("Graph API Error:", error);
    return { nodes: [], links: [] };
  }
};

// 🔹 Send chat query
export const sendQuery = async (question) => {
  try {
    const res = await API.post("/query", { question });

    console.log("QUERY RESPONSE:", res.data);

    return res.data;
  } catch (error) {
    console.error("Query API Error:", error);

    return {
      answer: "Error processing query. Please try again.",
    };
  }
};
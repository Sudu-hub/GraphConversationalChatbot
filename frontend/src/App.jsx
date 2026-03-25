import { useEffect, useState } from "react";
import GraphView from "./components/GraphView";
import ChatBox from "./components/ChatBox";
import { fetchGraph, sendQuery } from "./services/api";

function App() {
  const [graphData, setGraphData] = useState(null);
  const [highlightIds, setHighlightIds] = useState([]);
  const [highlightLinks, setHighlightLinks] = useState([]); // 🔥 NEW
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    fetchGraph()
      .then((data) => {
        console.log("GRAPH DATA:", data);
        setGraphData(data);
      })
      .catch((err) => {
        console.error("Graph fetch failed:", err);
      });
  }, []);

  const handleQuery = async (question) => {
    try {
      const res = await sendQuery(question);

      console.log("QUERY RESPONSE:", res);

      setHighlightIds(res?.ids || []);
      setHighlightLinks(res?.links || []); // 🔥 NEW

    } catch (err) {
      console.error("Query error:", err);
      setHighlightIds([]);
      setHighlightLinks([]);
    }
  };

  return (
    <div style={{ height: "100vh", background: "#f8fafc" }}>
      
      {/* HEADER */}
      <div style={{
        height: "50px",
        display: "flex",
        alignItems: "center",
        padding: "0 20px",
        borderBottom: "1px solid #e5e7eb"
      }}>
        Mapping / <b style={{ marginLeft: "5px" }}>Order to Cash</b>
      </div>

      {/* MAIN */}
      <div style={{ display: "flex", height: "calc(100vh - 50px)" }}>

        {/* GRAPH */}
        <div style={{ flex: 1, position: "relative" }}>
          <GraphView
            data={graphData}
            highlightIds={highlightIds}
            highlightLinks={highlightLinks} // 🔥 PASS
            onNodeClick={setSelectedNode}
          />

          {/* NODE DETAILS PANEL */}
          {selectedNode && (
            <div style={{
              position: "absolute",
              right: 20,
              top: 20,
              width: "260px",
              background: "white",
              border: "1px solid #e5e7eb",
              borderRadius: "8px",
              padding: "12px",
              boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
              zIndex: 20
            }}>
              <h4 style={{ marginBottom: "8px" }}>Node Details</h4>

              <p><b>ID:</b> {selectedNode.id}</p>
              <p><b>Type:</b> {selectedNode.type || "N/A"}</p>

              {selectedNode.data &&
                Object.entries(selectedNode.data).map(([k, v]) => (
                  <p key={k}><b>{k}:</b> {v}</p>
                ))
              }

              <button
                onClick={() => setSelectedNode(null)}
                style={{
                  marginTop: "10px",
                  padding: "6px 10px",
                  background: "#ef4444",
                  color: "white",
                  border: "none",
                  borderRadius: "6px",
                  cursor: "pointer"
                }}
              >
                Close
              </button>
            </div>
          )}
        </div>

        {/* CHAT */}
        <div style={{
          width: "350px",
          borderLeft: "1px solid #e5e7eb",
          background: "#ffffff"
        }}>
          <ChatBox onQuery={handleQuery} />
        </div>

      </div>
    </div>
  );
}

export default App;
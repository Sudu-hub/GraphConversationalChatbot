import { useEffect, useRef, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";

function GraphView({
  data,
  highlightIds = [],
  highlightLinks = [],
  onNodeClick
}) {
  const containerRef = useRef(null);
  const fgRef = useRef();

  const [size, setSize] = useState({ width: 800, height: 600 });

  // 🔥 Hover state
  const [hoverNode, setHoverNode] = useState(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // 🔥 Resize
  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        setSize({
          width: containerRef.current.offsetWidth,
          height: containerRef.current.offsetHeight,
        });
      }
    };

    updateSize();
    window.addEventListener("resize", updateSize);
    return () => window.removeEventListener("resize", updateSize);
  }, []);

  if (!data || !data.nodes) {
    return <p style={{ padding: "20px" }}>Loading graph...</p>;
  }

  return (
    <div
      ref={containerRef}
      style={{ width: "100%", height: "100%", position: "relative" }}
      onMouseMove={(e) => {
        setMousePos({ x: e.clientX, y: e.clientY });
      }}
    >
      <ForceGraph2D
        ref={fgRef}
        width={size.width}
        height={size.height}
        graphData={data}

        cooldownTicks={100}
        d3VelocityDecay={0.3}

        nodeAutoColorBy="type"
        nodeRelSize={6}

        linkColor={() => "#cbd5f5"}
        linkDirectionalArrowLength={4}
        linkDirectionalArrowRelPos={1}

        // 🔥 HOVER
        onNodeHover={(node) => {
          setHoverNode(node || null);
        }}

        // 🔥 CLICK
        onNodeClick={(node) => {
          if (fgRef.current) {
            fgRef.current.centerAt(node.x, node.y, 800);
            fgRef.current.zoom(2, 800);
          }
          if (onNodeClick) onNodeClick(node);
        }}

        // 🔥 NODE COLOR
        nodeColor={(node) => {
          if (!highlightIds?.length) return undefined;

          const id = node.id?.toString() || "";
          return highlightIds.some(h => id.includes(h))
            ? "#ef4444"
            : "#94a3b8";
        }}
      />

      {/* 🔥 BEAUTIFUL POPUP */}
      {hoverNode && (
        <div
          style={{
            position: "fixed",
            top: mousePos.y + 10,
            left: mousePos.x + 10,
            background: "white",
            padding: "12px",
            borderRadius: "10px",
            boxShadow: "0 8px 20px rgba(0,0,0,0.15)",
            fontSize: "12px",
            zIndex: 1000,
            minWidth: "220px",
            pointerEvents: "none"
          }}
        >
          <div style={{ fontWeight: "600", marginBottom: "6px" }}>
            {hoverNode.type || "Node"}
          </div>

          <div><b>ID:</b> {hoverNode.id}</div>

          {/* 🔥 dynamic fields */}
          {hoverNode.data &&
            Object.entries(hoverNode.data).slice(0, 6).map(([k, v]) => (
              <div key={k}>
                <b>{k}:</b> {String(v)}
              </div>
            ))}
        </div>
      )}
    </div>
  );
}

export default GraphView;
import { useEffect, useRef, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";

function GraphView({
  data,
  highlightIds = [],
  highlightLinks = [],   // 🔥 NEW
  onNodeClick
}) {
  const containerRef = useRef(null);
  const [size, setSize] = useState({ width: 800, height: 600 });

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
    <div ref={containerRef} style={{ width: "100%", height: "100%" }}>
      <ForceGraph2D
        width={size.width}
        height={size.height}
        graphData={data}

        nodeAutoColorBy="type"

        nodeLabel={(node) => `
          ID: ${node.id}
          Type: ${node.type || "N/A"}
        `}

        nodeRelSize={5}

        // 🔥 LINK HIGHLIGHT
        linkColor={(link) => {
          if (!highlightLinks || highlightLinks.length === 0) {
            return "#cbd5f5";
          }

          const sourceId = link.source.id || link.source;
          const targetId = link.target.id || link.target;

          const isMatch = highlightLinks.some(l =>
            l.source === sourceId && l.target === targetId
          );

          return isMatch ? "#ef4444" : "#e5e7eb";
        }}

        linkWidth={(link) => {
          const sourceId = link.source.id || link.source;
          const targetId = link.target.id || link.target;

          const isMatch = highlightLinks.some(l =>
            l.source === sourceId && l.target === targetId
          );

          return isMatch ? 3 : 1;
        }}

        linkDirectionalArrowLength={4}
        linkDirectionalArrowRelPos={1}

        onNodeClick={(node) => {
          if (onNodeClick) onNodeClick(node);
        }}

        // 🔥 NODE HIGHLIGHT
        nodeColor={(node) => {
          if (!highlightIds || highlightIds.length === 0) {
            return undefined;
          }

          const nodeId = node.id?.toString() || "";

          const isMatch = highlightIds.some(hid =>
            nodeId.includes(hid)
          );

          return isMatch ? "#ef4444" : "#94a3b8";
        }}

        nodeCanvasObject={(node, ctx) => {
          const nodeId = node.id?.toString() || "";

          const isMatch = highlightIds.some(hid =>
            nodeId.includes(hid)
          );

          if (isMatch) {
            ctx.fillStyle = "red";
            ctx.beginPath();
            ctx.arc(node.x, node.y, 6, 0, 2 * Math.PI);
            ctx.fill();
          }
        }}

        d3AlphaDecay={0.02}
      />
    </div>
  );
}

export default GraphView;
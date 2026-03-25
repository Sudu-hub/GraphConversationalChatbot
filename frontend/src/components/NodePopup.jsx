function NodePopup({ node, x, y }) {
  if (!node) return null;

  return (
    <div
      style={{
        position: "absolute",
        top: y,
        left: x,
        background: "#1f2937",
        color: "white",
        padding: "10px",
        borderRadius: "8px",
        fontSize: "12px",
        pointerEvents: "none",
        maxWidth: "250px",
        zIndex: 10
      }}
    >
      <strong>{node.id}</strong>
      <p>Type: {node.type}</p>

      {/* Show some data fields */}
      {node.data &&
        Object.entries(node.data).slice(0, 5).map(([key, value]) => (
          <div key={key}>
            <b>{key}:</b> {String(value)}
          </div>
        ))}
    </div>
  );
}

export default NodePopup;
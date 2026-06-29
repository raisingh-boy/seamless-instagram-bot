---
name: auto-memory
metadata:
  openclaw:
    emoji: "🧠"
    events: ["message:sent"]
---
// Auto-log every outbound message as a memory event
const handler = async (event) => {
  const { execSync } = await import("child_process");
  try {
    execSync(
      { timeout: 5000 }
    );
  } catch (e) {
    // silent fail
  }
};
export default handler;

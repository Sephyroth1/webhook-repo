import { useEffect, useState } from "react";

function App() {
  const [events, setEvents] = useState([]);

  const fetchEvents = async () => {
    try {
      const res = await fetch("https://a9462324ecaa.ngrok-free.app/events", {
        headers: {
          "ngrok-skip-browser-warning": "true",
        },
      });
      const data = await res.json();
      setEvents(data); // setState is now inside a callback
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    // run once on mount

    // then poll every 15 seconds
    const interval = setInterval(() => {
      fetchEvents();
    }, 15000);

    fetchEvents();
    // cleanup
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      style={{
        maxWidth: "600px",
        margin: "40px auto",
        padding: "20px",
        border: "1px solid #ddd",
        borderRadius: "8px",
        fontFamily: "Arial",
      }}
    >
      <h2>GitHub Events</h2>
      {events.map((e, i) => {
        let text = "";
        if (e.action === "PUSH") {
          text = `${e.author} pushed to ${e.to_branch} on ${e.timestamp}`;
        } else if (e.action === "PULL_REQUEST") {
          text = `${e.author} submitted a pull request from ${e.from_branch} to ${e.to_branch} on ${e.timestamp}`;
        } else if (e.action === "MERGE") {
          text = `${e.author} merged branch ${e.from_branch} to ${e.to_branch} on ${e.timestamp}`;
        }
        return (
          <p key={i} style={{ fontSize: "16px", textAlign: "left" }}>
            {text}
          </p>
        );
      })}
    </div>
  );
}

export default App;

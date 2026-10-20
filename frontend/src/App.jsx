
import { useState } from "react";
import { useConversation } from "@elevenlabs/react";
import "./App.css";

function App() {
  const [error, setError] = useState("");
  const [starting, setStarting] = useState(false);

  const conversation = useConversation({
    onConnect: () => {
      setError("");
      setStarting(false);
    },
    onDisconnect: () => setStarting(false),
    onError: (message) => {
      setError(
        typeof message === "string"
          ? message
          : "Voice connection failed. Please try again."
      );
      setStarting(false);
    },
  });

  async function startCall() {
    setError("");
    setStarting(true);

    try {
      const baseUrl =
        import.meta.env.VITE_API_BASE_URL ||
        "http://localhost:8000";

      // Request microphone permission after a user action.
      await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      const response = await fetch(
        `${baseUrl}/api/voice/signed-url`
      );

      if (!response.ok) {
        throw new Error(
          "Voice session nahi ban paya. Backend check karo."
        );
      }

      const data = await response.json();

      if (!data.signed_url) {
        throw new Error("Signed URL response missing hai.");
      }

      await conversation.startSession({
        signedUrl: data.signed_url,
      });
    } catch (err) {
      console.error(err);
      setError(
        err instanceof Error
          ? err.message
          : "Voice assistant start nahi ho paya."
      );
      setStarting(false);
    }
  }

  async function endCall() {
    try {
      await conversation.endSession();
    } catch (err) {
      console.error(err);
      setError("Call end karte waqt error aaya.");
    }
  }

  const connected = conversation.status === "connected";
  const busy =
    starting || conversation.status === "connecting";

  return (
    <main className="app">
      <nav className="navbar">
        <div className="brand">
          <span className="brand-icon">A</span>
          <span>Aitlas AI</span>
        </div>
        <span className="language">Hindi · English</span>
      </nav>

      <section className="hero">
        <div className="eyebrow">
          YOUR AI CUSTOMER SUPPORT ASSISTANT
        </div>

        <h1>
          How can we
          <br />
          <span>help you today?</span>
        </h1>

        <p className="subtitle">
          Talk naturally in Hindi, English, or Hinglish.
          Our AI assistant is here to help with your questions.
        </p>

        <div className={`orb ${connected ? "active" : ""}`}>
          <div className="orb-inner">
            <span>{connected ? "🎙️" : "🎧"}</span>
          </div>
        </div>

        <p className="call-status" role="status">
          {busy
            ? "Connecting to your assistant..."
            : connected
              ? "Connected — boliye, main sun raha hoon"
              : "Ready when you are"}
        </p>

        <div className="actions">
          {!connected ? (
            <button
              className="primary-button"
              onClick={startCall}
              disabled={busy}
            >
              {busy ? "Connecting..." : "Start conversation"}
            </button>
          ) : (
            <button
              className="end-button"
              onClick={endCall}
            >
              End conversation
            </button>
          )}
        </div>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        <p className="privacy">
          AI-powered support · Please don't share passwords,
          OTPs, or payment PINs.
        </p>
      </section>

      <section className="features">
        <article>
          <span>💬</span>
          <h2>Instant answers</h2>
          <p>Get help with common customer questions.</p>
        </article>

        <article>
          <span>📦</span>
          <h2>Order assistance</h2>
          <p>Check order status after verification.</p>
        </article>

        <article>
          <span>🎧</span>
          <h2>Human support</h2>
          <p>Raise a ticket when you need more help.</p>
        </article>
      </section>

      <footer>
        Aitlas AI · Customer support made conversational
      </footer>
    </main>
  );
}

export default App;

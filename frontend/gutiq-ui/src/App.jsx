import { useState } from "react";
import EventForm from "./components/EventForm";
import EventList from "./components/EventList";
import "./App.css";

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleEventCreated = () => {
    // Trigger a refresh of the event list
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="app">
      <header>
        <h1>GutIQ</h1>
        <p className="subtitle">Track your meals, exercise, and GI symptoms</p>
      </header>

      <main className="container">
        <div className="layout">
          <div className="left-panel">
            <EventForm onEventCreated={handleEventCreated} />
          </div>
          <div className="right-panel">
            <EventList refreshTrigger={refreshTrigger} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
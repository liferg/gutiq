import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import EventForm from "./components/EventForm";
import EventList from "./components/EventList";
import AIInsights from "./components/AIInsights";
import "./App.css";

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // Data is fresh for 5 minutes
      refetchOnWindowFocus: true, // Refetch when window regains focus
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="app">
        <header>
          <h1>GutIQ</h1>
          <p className="subtitle">Track your meals, exercise, and GI symptoms</p>
        </header>

        <main className="container">
          <AIInsights />

          <div className="layout">
            <div className="left-panel">
              <EventForm />
            </div>
            <div className="right-panel">
              <EventList />
            </div>
          </div>
        </main>
      </div>
    </QueryClientProvider>
  );
}

export default App;
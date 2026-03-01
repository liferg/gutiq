import { useQuery } from "@tanstack/react-query";
import api from "../services/api";
import "./AIInsights.css";

function AIInsights() {
  // Fetch the most recent insight
  const { data: insights = [], isLoading, error } = useQuery({
    queryKey: ["insights"],
    queryFn: () => api.getInsights(),
  });

  // Get the most recent insight
  const latestInsight = insights.length > 0 ? insights[0] : null;

  if (isLoading) {
    return (
      <div className="ai-insights-card">
        <h2>AI Insights</h2>
        <p className="loading-message">Loading insights...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="ai-insights-card">
        <h2>AI Insights</h2>
        <p className="error-message">Error loading insights: {error.message}</p>
      </div>
    );
  }

  return (
    <div className="ai-insights-card">
      <div className="insights-header">
        <h2>AI Insights</h2>
      </div>

      {latestInsight ? (
        <div className="insight-content">
          <p className="insight-timestamp">
            {new Date(latestInsight.timestamp).toLocaleString()}
          </p>
          <p className="insight-text">{latestInsight.description}</p>
        </div>
      ) : (
        <div className="empty-state">
          <p className="empty-message">
            No insights yet. Keep logging your meals, exercises, and symptoms to build up data.
          </p>
          <p className="empty-submessage">
            AI insights are automatically generated after every 40 meal events logged.
          </p>
        </div>
      )}
    </div>
  );
}

export default AIInsights;

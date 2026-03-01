import { useQuery } from "@tanstack/react-query";
import { useState, useEffect } from "react";
import api from "../services/api";
import "./AIInsights.css";

function AIInsights() {
  const [isGenerating, setIsGenerating] = useState(false);

  // Fetch the most recent insight
  // Refetch every 2 seconds when generating
  const { data: insights = [], isLoading, error } = useQuery({
    queryKey: ["insights"],
    queryFn: () => api.getInsights(),
    refetchInterval: isGenerating ? 2000 : false,
  });

  // Get the most recent insight
  const latestInsight = insights.length > 0 ? insights[0] : null;

  // Listen for meal event creations to trigger generating state
  useEffect(() => {
    const handleInsightGeneration = () => {
      console.log("AIInsights: Received insight-generation-started event");
      setIsGenerating(true);
      // Stop polling after 30 seconds max
      setTimeout(() => {
        console.log("AIInsights: Timeout - stopping generation state");
        setIsGenerating(false);
      }, 30000);
    };

    console.log("AIInsights: Setting up event listener");
    window.addEventListener("insight-generation-started", handleInsightGeneration);
    return () => {
      console.log("AIInsights: Cleaning up event listener");
      window.removeEventListener("insight-generation-started", handleInsightGeneration);
    };
  }, []);

  // Stop generating state when we get a new insight
  useEffect(() => {
    if (latestInsight && isGenerating) {
      setIsGenerating(false);
    }
  }, [latestInsight, isGenerating]);

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
        {isGenerating && (
          <span className="generating-badge">Generating new insight...</span>
        )}
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

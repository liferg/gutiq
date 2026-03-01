import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

const EventList = () => {
  const queryClient = useQueryClient();

  const {
    data: events = [],
    isLoading: loading,
    error,
  } = useQuery({
    queryKey: ["events"],
    queryFn: () => api.getEvents(),
  });

  const deleteEventMutation = useMutation({
    mutationFn: (eventId) => api.deleteEvent(eventId),
    onSuccess: () => {
      // Invalidate and refetch events
      queryClient.invalidateQueries({ queryKey: ["events"] });
    },
    onError: (err) => {
      console.error("Error deleting event:", err);
      alert(`Failed to delete event: ${err.message}`);
    },
  });

  const handleDelete = (eventId, eventType) => {
    if (window.confirm(`Are you sure you want to delete this ${eventType}?`)) {
      deleteEventMutation.mutate(eventId);
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
  };

  const formatEventType = (type) => {
    return type.charAt(0).toUpperCase() + type.slice(1);
  };

  const renderEventData = (event) => {
    if (event.event_type === "meal") {
      const nutritionItems = [];
      if (event.data.calories) nutritionItems.push(`${event.data.calories} cal`);
      if (event.data.protein) nutritionItems.push(`Protein: ${event.data.protein}g`);
      if (event.data.carbohydrates) nutritionItems.push(`Carbs: ${event.data.carbohydrates}g`);
      if (event.data.fats) nutritionItems.push(`Fats: ${event.data.fats}g`);

      return (
        <div className="event-details">
          <ul>
            <li><strong>Foods:</strong> {event.data.foods.join(", ")}</li>
            {nutritionItems.length > 0 && (
              <li><strong>Nutrition:</strong> {nutritionItems.join(" | ")}</li>
            )}
          </ul>
        </div>
      );
    } else if (event.event_type === "exercise") {
      return (
        <div className="event-details">
          <ul>
            <li><strong>Type:</strong> {event.data.type}</li>
            <li><strong>Duration:</strong> {event.data.duration_minutes} minutes</li>
          </ul>
        </div>
      );
    } else if (event.event_type === "symptom") {
      return (
        <div className="event-details">
          <ul>
            <li><strong>Description:</strong> {event.data.description}</li>
            <li>
              <strong>Severity:</strong>{" "}
              <span className={`severity-badge ${event.data.severity}`}>
                {event.data.severity}
              </span>
            </li>
          </ul>
        </div>
      );
    }
  };

  if (loading) {
    return <div className="event-list loading">Loading events...</div>;
  }

  if (error) {
    return <div className="event-list error">Error: {error.message}</div>;
  }

  return (
    <div className="event-list">
      <h2>Recent Events</h2>

      {events.length === 0 ? (
        <p className="no-events">No events logged yet. Start by adding one!</p>
      ) : (
        <div className="events">
          {events.map((event) => (
            <div key={event.event_id} className={`event-card ${event.event_type}`}>
              <div className="event-header">
                <h3 className="event-title">
                  {formatEventType(event.event_type)}: {formatTimestamp(event.timestamp)}
                </h3>
                <button
                  onClick={() => handleDelete(event.event_id, event.event_type)}
                  className="delete-button"
                  disabled={deleteEventMutation.isPending}
                  title="Delete event"
                >
                  ×
                </button>
              </div>
              {renderEventData(event)}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default EventList;

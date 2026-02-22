import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

const EventForm = () => {
  const queryClient = useQueryClient();
  const [eventType, setEventType] = useState("meal");

  // Get current time in local timezone for datetime-local input
  const getLocalDateTime = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  };

  const [timestamp, setTimestamp] = useState(getLocalDateTime());

  // Meal fields
  const [foods, setFoods] = useState("");
  const [calories, setCalories] = useState("");
  const [protein, setProtein] = useState("");
  const [carbohydrates, setCarbohydrates] = useState("");
  const [fats, setFats] = useState("");

  // Exercise fields
  const [exerciseType, setExerciseType] = useState("");
  const [durationMinutes, setDurationMinutes] = useState("");

  // Symptom fields
  const [description, setDescription] = useState("");
  const [severity, setSeverity] = useState("mild");

  const createEventMutation = useMutation({
    mutationFn: (eventData) => api.createEvent(eventData),
    onSuccess: (result) => {
      console.log("Event created:", result);
      // Invalidate and refetch events query
      queryClient.invalidateQueries({ queryKey: ["events"] });
      // Clear form
      resetForm();
    },
    onError: (err) => {
      console.error("Error creating event:", err);
    },
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    let eventData = {
      timestamp: new Date(timestamp).toISOString(),
      event_type: eventType,
      data: {},
    };

    // Build the data object based on event type
    if (eventType === "meal") {
      eventData.data = {
        foods: foods.split(",").map((f) => f.trim()),
        calories: calories ? parseFloat(calories) : null,
        protein: protein ? parseFloat(protein) : null,
        carbohydrates: carbohydrates ? parseFloat(carbohydrates) : null,
        fats: fats ? parseFloat(fats) : null,
      };
    } else if (eventType === "exercise") {
      eventData.data = {
        type: exerciseType,
        duration_minutes: parseFloat(durationMinutes),
      };
    } else if (eventType === "symptom") {
      eventData.data = {
        description,
        severity,
      };
    }

    createEventMutation.mutate(eventData);
  };

  const resetForm = () => {
    setTimestamp(getLocalDateTime());
    setFoods("");
    setCalories("");
    setProtein("");
    setCarbohydrates("");
    setFats("");
    setExerciseType("");
    setDurationMinutes("");
    setDescription("");
    setSeverity("mild");
  };

  return (
    <div className="event-form">
      <h2>Log New Event</h2>

      <form onSubmit={handleSubmit}>
        {/* Event Type Selector */}
        <div className="form-group">
          <label>Event Type:</label>
          <div className="event-type-tabs">
            <button
              type="button"
              className={eventType === "meal" ? "active" : ""}
              onClick={() => setEventType("meal")}
            >
              Meal
            </button>
            <button
              type="button"
              className={eventType === "exercise" ? "active" : ""}
              onClick={() => setEventType("exercise")}
            >
              Exercise
            </button>
            <button
              type="button"
              className={eventType === "symptom" ? "active" : ""}
              onClick={() => setEventType("symptom")}
            >
              Symptom
            </button>
          </div>
        </div>

        {/* Timestamp */}
        <div className="form-group">
          <label>When:</label>
          <input
            type="datetime-local"
            value={timestamp}
            onChange={(e) => setTimestamp(e.target.value)}
            required
          />
        </div>

        {/* Meal Fields */}
        {eventType === "meal" && (
          <>
            <div className="form-group">
              <label>Foods (comma-separated):</label>
              <input
                type="text"
                value={foods}
                onChange={(e) => setFoods(e.target.value)}
                placeholder="e.g., greek yogurt, banana, granola"
                required
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Calories:</label>
                <input
                  type="number"
                  value={calories}
                  onChange={(e) => setCalories(e.target.value)}
                  placeholder="Optional"
                />
              </div>
              <div className="form-group">
                <label>Protein (g):</label>
                <input
                  type="number"
                  value={protein}
                  onChange={(e) => setProtein(e.target.value)}
                  placeholder="Optional"
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Carbs (g):</label>
                <input
                  type="number"
                  value={carbohydrates}
                  onChange={(e) => setCarbohydrates(e.target.value)}
                  placeholder="Optional"
                />
              </div>
              <div className="form-group">
                <label>Fats (g):</label>
                <input
                  type="number"
                  value={fats}
                  onChange={(e) => setFats(e.target.value)}
                  placeholder="Optional"
                />
              </div>
            </div>
          </>
        )}

        {/* Exercise Fields */}
        {eventType === "exercise" && (
          <>
            <div className="form-group">
              <label>Exercise Type:</label>
              <input
                type="text"
                value={exerciseType}
                onChange={(e) => setExerciseType(e.target.value)}
                placeholder="e.g., running, weight lifting"
                required
              />
            </div>
            <div className="form-group">
              <label>Duration (minutes):</label>
              <input
                type="number"
                value={durationMinutes}
                onChange={(e) => setDurationMinutes(e.target.value)}
                placeholder="e.g., 30"
                required
              />
            </div>
          </>
        )}

        {/* Symptom Fields */}
        {eventType === "symptom" && (
          <>
            <div className="form-group">
              <label>Description:</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe your symptom..."
                required
                rows="3"
              />
            </div>
            <div className="form-group">
              <label>Severity:</label>
              <select
                value={severity}
                onChange={(e) => setSeverity(e.target.value)}
              >
                <option value="mild">Mild</option>
                <option value="moderate">Moderate</option>
                <option value="severe">Severe</option>
              </select>
            </div>
          </>
        )}

        {createEventMutation.isError && (
          <div className="error-message">{createEventMutation.error.message}</div>
        )}

        <button
          type="submit"
          disabled={createEventMutation.isPending}
          className="submit-btn"
        >
          {createEventMutation.isPending ? "Saving..." : "Log Event"}
        </button>
      </form>
    </div>
  );
};

export default EventForm;

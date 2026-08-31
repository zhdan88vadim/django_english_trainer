import { useState, useEffect, useRef } from "react";
import { TaskStatus } from "../types/video";
import videoApi from "../services/generateVideoService";

export const useTaskPolling = (
  taskId: string | null,
  onComplete?: (status: TaskStatus) => void,
  onError?: (error: Error) => void
) => {
  const [status, setStatus] = useState<TaskStatus | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const isMountedRef = useRef(true);

  useEffect(() => {
    // Clear any existing interval when taskId changes
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    if (!taskId) {
      setIsPolling(false);
      setStatus(null);
      return;
    }

    setIsPolling(true);
    isMountedRef.current = true;

    const poll = async () => {
      try {
        const result = await videoApi.getTaskStatus(taskId);

        // Only update if component is still mounted
        if (!isMountedRef.current) return;

        setStatus(result);

        const isComplete = result.status === "completed";
        const isError = result.status === "failed";

        if (isComplete || isError) {
          setIsPolling(false);
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
          }

          if (isComplete && onComplete) {
            onComplete(result);
          }
          if (isError && onError) {
            onError(new Error(result.message || "Task failed"));
          }
        }
      } catch (error) {
        console.error("Polling error:", error);
        if (!isMountedRef.current) return;

        setIsPolling(false);
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
        if (onError) {
          onError(error instanceof Error ? error : new Error("Unknown error"));
        }
      }
    };

    // Initial poll
    poll();

    // Set up interval
    intervalRef.current = setInterval(poll, 3000);

    return () => {
      isMountedRef.current = false;
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      setIsPolling(false);
    };
  }, [taskId]);

  return { status, isPolling };
};

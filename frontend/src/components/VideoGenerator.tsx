import React, { useState } from 'react';
import { TaskStatus } from './TaskStatus';
import videoApi from '../services/generateVideoService';
import { useTaskPolling } from '../hooks/useTaskPolling';

export const VideoGenerator: React.FC = () => {
  const [text, setText] = useState('Привет мир;Hello world');
  const [taskId, setTaskId] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!text.trim()) {
      setError('Please enter some text');
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      const response = await videoApi.generateVideoFromText(text);
      setTaskId(response.task_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start generation');
      setIsGenerating(false);
    }
  };

  const handleTaskComplete = () => {
    setIsGenerating(false);
  };

  const handleTaskError = (err: Error) => {
    setError(err.message);
    setIsGenerating(false);
  };

  const { status, isPolling } = useTaskPolling(
    taskId,
    handleTaskComplete,
    handleTaskError
  );

  const resetForm = () => {
    setText('');
    setTaskId(null);
    setError(null);
    setIsGenerating(false);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Generate Video from Text
        </h2>

        <div className="space-y-6">
          {/* Text Input */}
          <div>
            <label htmlFor="text-input" className="block text-sm font-medium text-gray-700 mb-2">
              Enter your text
            </label>
            <textarea
              id="text-input"
              rows={6}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter the text you want to convert to video..."
              value={text}
              onChange={handleTextChange}
              disabled={isGenerating || isPolling}
            />
            <div className="mt-1 text-sm text-gray-500">
              {text.split('\n').filter(line => line.trim()).length} lines
            </div>
          </div>

          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            </div>
          )}

          {!taskId && !isGenerating && (
            <div className="flex space-x-4">
              <button
                onClick={handleSubmit}
                disabled={!text.trim()}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                Generate Video
              </button>
              <button
                onClick={resetForm}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
              >
                Clear
              </button>
            </div>
          )}

          {isGenerating && (
            <div className="text-center text-sm text-gray-500">
              Starting video generation...
            </div>
          )}

          <TaskStatus
            status={status}
            isPolling={isPolling}
            onDownload={() => {
              setTimeout(resetForm, 3000);
            }}
          />

          {status?.status === 'completed' && (
            <div className="mt-4 text-center">
              <button
                onClick={resetForm}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                Generate Another Video
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
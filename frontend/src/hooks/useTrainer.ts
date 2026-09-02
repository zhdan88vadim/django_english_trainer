import { useState, useEffect, useCallback, useRef } from 'react';
import { Word } from '../types';
import apiService from '../services/api';

interface UseTrainerReturn {
  words: Word[];
  currentIndex: number;
  currentPage: number;
  hasMore: boolean;
  isLoading: boolean;
  isRevealed: boolean;
  total: number;
  error: string | null;
  currentWord: Word | null;
  currentPosition: number;
  timeRemaining: number;
  isTimerRunning: boolean;
  setIsTimerRunning: (running: boolean) => void;
  resetTimer: () => void;
  revealWord: () => void;
  nextWord: () => void;
  resetTrainer: () => void;
  fetchWords: (page: number, categoryId?: number | null) => Promise<void>;
}

const LIMIT = 100;
const DEFAULT_DURATION = 60; // Timer duration in seconds

export const useTrainer = (categoryId?: number | null): UseTrainerReturn => {
  const [words, setWords] = useState<Word[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isRevealed, setIsRevealed] = useState<boolean>(false);
  const [total, setTotal] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  const [timeRemaining, setTimeRemaining] = useState<number>(DEFAULT_DURATION);
  const [isTimerRunning, setIsTimerRunning] = useState<boolean>(true);
  
  const timerIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const tickRef = useRef<() => void>(() => {});

  const currentWord: Word | null = words.length > 0 ? words[currentIndex] : null;

  const resetTimer = useCallback(() => {
    setTimeRemaining(DEFAULT_DURATION);
  }, []);

  const revealWord = useCallback((): void => {
    setIsRevealed(true);
    resetTimer();
  }, [resetTimer]);

  const nextWord = useCallback((): void => {
    if (currentIndex + 1 >= words.length) {
      if (hasMore) {
        fetchWords(currentPage + 1, categoryId);
        return;
      } else {
        setWords([]);
        setIsTimerRunning(false);
        return;
      }
    }

    setCurrentIndex((prev) => prev + 1);
    setIsRevealed(false);
    resetTimer();
  }, [currentIndex, words.length, hasMore, currentPage, categoryId, resetTimer]);


  const performScheduledAction = useCallback(() => {
    console.log('performScheduledAction', { isRevealed, hasWords: words.length > 0 });
    
    if (!isRevealed && words.length > 0 && currentWord) {
      revealWord();
    } else if (isRevealed && words.length > 0) {
      nextWord();
    } else {
      setIsTimerRunning(false);
    }
  }, [isRevealed, words.length, currentWord, revealWord, nextWord]);

  const handleTimerTick = () => {
    setTimeRemaining((prev) => {
      console.log('handleTimerTick', prev);
      
      if (prev <= 1) {
        performScheduledAction();
        return DEFAULT_DURATION;
      }
      return prev - 1;
    });
  };

  useEffect(() => {
    tickRef.current = handleTimerTick;
  });

  useEffect(() => {
    if (isTimerRunning && words.length > 0 && currentWord) {
      timerIntervalRef.current = setInterval(() => tickRef.current(), 1000);
    }

    return () => {
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
        timerIntervalRef.current = null;
      }
    };
  }, [isTimerRunning, words.length, !!currentWord]);

  const fetchWords = useCallback(async (page: number = 1, categoryId?: number | null): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);

      const data = await apiService.fetchRandomWords(LIMIT, categoryId);
      
      setWords(data.results);
      setTotal(data.total);
      setHasMore(data.has_more);
      setCurrentPage(page);
      setCurrentIndex(0);
      setIsRevealed(false);
      resetTimer();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load words';
      setError(errorMessage);
      console.error('Error fetching words:', err);
    } finally {
      setIsLoading(false);
    }
  }, [resetTimer]);

  // Load initial words
  useEffect(() => {
    fetchWords(1, categoryId);
  }, [fetchWords, categoryId]);

  const resetTrainer = useCallback((): void => {
    fetchWords(1, categoryId);
  }, [fetchWords, categoryId]);

  const currentPosition: number = currentWord ? (currentPage - 1) * LIMIT + currentIndex + 1 : 0;

  return {
    words,
    currentIndex,
    currentPage,
    hasMore,
    isLoading,
    isRevealed,
    total,
    error,
    currentWord,
    currentPosition,
    timeRemaining, 
    isTimerRunning,
    setIsTimerRunning,
    resetTimer,
    revealWord,
    nextWord,
    resetTrainer,
    fetchWords,
  };
};

// hooks/useTrainer.ts
import { useState, useEffect, useCallback } from 'react';
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
  revealWord: () => void;
  nextWord: () => void;
  resetTrainer: () => void;
  fetchWords: (page: number) => Promise<void>;
}

const LIMIT = 100;

export const useTrainer = (): UseTrainerReturn => {
  const [words, setWords] = useState<Word[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isRevealed, setIsRevealed] = useState<boolean>(false);
  const [total, setTotal] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  const fetchWords = useCallback(async (page: number = 1): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);

      const data = await apiService.fetchRandomWords(LIMIT);
      
      setWords(data.results);
      setTotal(data.total);
      setHasMore(data.has_more);
      setCurrentPage(page);
      setCurrentIndex(0);
      setIsRevealed(false);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load words';
      setError(errorMessage);
      console.error('Error fetching words:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Load initial words
  useEffect(() => {
    fetchWords(1);
  }, [fetchWords]);

  const revealWord = useCallback((): void => {
    setIsRevealed(true);
  }, []);

  const nextWord = useCallback((): void => {
    // Check if we need to load more words
    if (currentIndex + 1 >= words.length) {
      if (hasMore) {
        fetchWords(currentPage + 1);
        return;
      } else {
        // No more words - clear state to show completion
        setWords([]);
        return;
      }
    }

    setCurrentIndex((prev) => prev + 1);
    setIsRevealed(false);
  }, [currentIndex, words.length, hasMore, currentPage, fetchWords]);

  const resetTrainer = useCallback((): void => {
    fetchWords(1);
  }, [fetchWords]);

  const currentWord: Word | null = words.length > 0 ? words[currentIndex] : null;
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
    revealWord,
    nextWord,
    resetTrainer,
    fetchWords,
  };
};
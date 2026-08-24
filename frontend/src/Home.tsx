// Home.tsx
import React, { useEffect } from 'react';
import { useTrainer } from './hooks/useTrainer';
import { useAuth } from './context/AuthContext';
import './Home.scss';

const Home: React.FC = () => {
  const {
    words,
    currentWord,
    currentPosition,
    total,
    isLoading,
    isRevealed,
    error,
    revealWord,
    nextWord,
    resetTrainer,
    fetchWords,
  } = useTrainer();

  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent): void => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        if (!isRevealed && words.length > 0 && currentWord) {
          revealWord();
        } else if (isRevealed && words.length > 0) {
          nextWord();
        }
      }
    };

    document.addEventListener('keydown', handleKeyPress);
    return () => document.removeEventListener('keydown', handleKeyPress);
  }, [isRevealed, words.length, currentWord, revealWord, nextWord]);

  // Loading state
  if (isLoading) {
    return (
      <div className="container">
        <h1>📚 English Trainer</h1>
        <div className="card">
          <div className="loading">Loading words...</div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="container">
        <h1>📚 English Trainer</h1>
        <div className="card">
          <div className="empty-state">
            <span className="emoji">❌</span>
            <p>{error}</p>
            <button className="btn-primary" onClick={() => fetchWords(1)}>
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Completion state (all words reviewed)
  if (words.length === 0 && !isLoading) {
    return (
      <div className="container">
        <h1>📚 English Trainer</h1>
        <div className="card">
          <div className="empty-state">
            <span className="emoji">🎉</span>
            <p>Congratulations! You've reviewed all words!</p>
            <button className="btn-primary" onClick={resetTrainer}>
              Start Over
            </button>
          </div>
        </div>
      </div>
    );
  }

  // No words in database
  if (!currentWord) {
    return (
      <div className="container">
        <h1>📚 English Trainer</h1>
        <div className="card">
          <div className="empty-state">
            <span className="emoji">📝</span>
            <p>No words yet. Add some words to start learning!</p>
          </div>
        </div>
      </div>
    );
  }

  return (
   
    <div className="container">

      <nav className="navbar">
        <div className="nav-brand">
        </div>
        <div className="nav-user">
          <span className="user-email">{user?.email}</span>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </nav>

      <h1>📚 English Trainer</h1>
     
      <div className="card">
        <div className="progress">
          {currentPosition} / {total} words
        </div>

        <div className="translation-display">
          {currentWord.translation}
        </div>

        <div className={`word-display ${isRevealed ? 'visible' : 'hidden'}`}>
          {isRevealed ? currentWord.word : '❓'}
        </div>

        <div className="btn-group">
          {!isRevealed ? (
            <button className="btn-primary" onClick={revealWord}>
              Show Word
            </button>
          ) : (
            <button className="btn-success" onClick={nextWord}>
              Next →
            </button>
          )}
        </div>

        <div className="hint">
          Press <kbd>Space</kbd> or <kbd>Enter</kbd> to interact
        </div>
      </div>
    </div>
  );
};

export default Home;
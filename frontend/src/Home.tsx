// Home.tsx
import React, { useEffect, useState } from 'react';
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

  // Font size states
  const [questionFontSize, setQuestionFontSize] = useState(80);
  const [answerFontSize, setAnswerFontSize] = useState(80);

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
      // Font size controls
      if (e.key === 'ArrowUp' && e.shiftKey) {
        e.preventDefault();
        setAnswerFontSize(prev => Math.min(prev + 4, 120));
        setQuestionFontSize(prev => Math.min(prev + 4, 120));
      }
      if (e.key === 'ArrowDown' && e.shiftKey) {
        e.preventDefault();
        setAnswerFontSize(prev => Math.max(prev - 4, 20));
        setQuestionFontSize(prev => Math.max(prev - 4, 20));
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
          <h1>📚 English Trainer</h1>
        </div>
        <div className="nav-user">
          <span className="user-email">{user?.email}</span>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </nav>

      <div className="card">
        <div className="progress">
          {currentPosition} / {total} words
        </div>

        <div className="content-area">
          <div 
            className="translation-display"
            style={{ fontSize: `${questionFontSize}px` }}
          >
            {currentWord.translation}
          </div>

          <div 
            className={`word-display ${isRevealed ? 'visible' : 'hidden'}`}
            style={{ fontSize: `${answerFontSize}px` }}
          >
            {isRevealed ? currentWord.word : '❓'}
          </div>
        </div>

        {/* Fixed position button */}
        <div className="btn-group">
          {!isRevealed ? (
            <button className="btn" onClick={revealWord}>
              Show Word
            </button>
          ) : (
            <button className="btn" onClick={nextWord}>
              Next →
            </button>
          )}
        </div>

        <div className="controls-hint">
          <div className="hint">
            Press <kbd>Space</kbd> or <kbd>Enter</kbd> to interact
          </div>
          <div className="hint font-controls">
            <span>Font size: </span>
            <button 
              className="font-btn" 
              onClick={() => {
                setAnswerFontSize(prev => Math.max(prev - 4, 20));
                setQuestionFontSize(prev => Math.max(prev - 4, 20));
              }}
            >
              A-
            </button>
            <button 
              className="font-btn" 
              onClick={() => {
                setAnswerFontSize(prev => Math.min(prev + 4, 120));
                setQuestionFontSize(prev => Math.min(prev + 4, 120));
              }}
            >
              A+
            </button>
            <span className="font-size-label">
              {!isRevealed ? questionFontSize : answerFontSize}px
            </span>
            <span className="font-target">
              ({!isRevealed ? 'Question' : 'Answer'})
            </span>
          </div>
          <div className="hint">
            <kbd>Shift</kbd> + <kbd>↑</kbd> / <kbd>↓</kbd> to adjust
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
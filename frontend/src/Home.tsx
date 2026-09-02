import React, { useEffect, useState } from 'react';
import { useTrainer } from './hooks/useTrainer';
import { useAuth } from './context/AuthContext';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';

import './Home.scss';

const Home: React.FC = () => {
  const [searchParams] = useSearchParams();
  const categoryId = searchParams.get('category_id');
  const categoryIdInt = categoryId ? parseInt(categoryId) : null;

  const {
    words,
    currentWord,
    currentPosition,
    timeRemaining,       
    isTimerRunning,      
    setIsTimerRunning,   
    resetTimer,              
    total,
    isLoading,
    isRevealed,
    error,
    revealWord,
    nextWord,
    resetTrainer,
    fetchWords,
  } = useTrainer(categoryIdInt);
  
  const { user, logout } = useAuth();

  // Font size states
  const [questionFontSize, setQuestionFontSize] = useState(8);
  const [answerFontSize, setAnswerFontSize] = useState(8);
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
  };

  const handleBackToCategories = () => {
    navigate('/categories');
  };


  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent): void => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        resetTimer();
        
        if (!isRevealed && words.length > 0 && currentWord) {
          revealWord();
        } else if (isRevealed && words.length > 0) {
          nextWord();
        }
      }
      
      if (e.key === 'ArrowUp' && e.shiftKey) {
        e.preventDefault();
        setAnswerFontSize(prev => Math.min(prev + 0.5, 15));
        setQuestionFontSize(prev => Math.min(prev + 0.5, 15));
      }
      
      if (e.key === 'ArrowDown' && e.shiftKey) {
        e.preventDefault();
        setAnswerFontSize(prev => Math.max(prev - 0.5, 2));
        setQuestionFontSize(prev => Math.max(prev - 0.5, 2));
      }
    };

    document.addEventListener('keydown', handleKeyPress);
    return () => document.removeEventListener('keydown', handleKeyPress);
  }, [isRevealed, words.length, currentWord, revealWord, nextWord]);

  const handleManualAction = (action: () => void) => {
    resetTimer();
    action();
  };

  const handleTimerToggle = () => {
    setIsTimerRunning(!isTimerRunning);
  };
  // Loading state
  if (isLoading) {
    return (
      <div className="app fullscreen">
        <h1>📚 English Trainer</h1>
        <div className="card fullscreen-card">
          <div className="loading">Loading words...</div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="app fullscreen">
        <h1>📚 English Trainer</h1>
        <div className="card fullscreen-card">
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

  // Completion state
  if (words.length === 0 && !isLoading) {
    return (
      <div className="app fullscreen">
        <h1>📚 English Trainer</h1>
        <div className="card fullscreen-card">
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

  // No words state
  if (!currentWord) {
    return (
      <div className="app fullscreen">
        <h1>📚 English Trainer</h1>
        <div className="card fullscreen-card">
          <div className="empty-state">
            <span className="emoji">📝</span>
            <p>No words yet. Add some words to start learning!</p>
          </div>
        </div>
      </div>
    );
  }

  // Main render
  return (
    <div className="app fullscreen">
      <nav className="navbar fullscreen-nav">
        <div className="nav-brand">
          <h1>📚 English Trainer</h1>
        </div>
        <div>
          <div className="btn-group fullscreen-buttons">
            <Link to="/generate" className="btn fullscreen-btn">
              Generate
            </Link>                        
            <button 
              className="btn fullscreen-btn" 
              onClick={handleBackToCategories}
            >
              📂 Categories
            </button>

            {!isRevealed ? (
              <button 
                className="btn fullscreen-btn" 
                onClick={() => handleManualAction(revealWord)}
              >
                Show Word
              </button>
            ) : (
              <button 
                className="btn fullscreen-btn" 
                onClick={() => handleManualAction(nextWord)}
              >
                Next →
              </button>
            )}
          </div>
        </div>
        <div className="nav-user">
          <span className="user-email">{user?.email}</span>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </nav>

      <div className="card fullscreen-card">
        {/* Timer */}
        <div className="timer-container">
          <div className="timer-progress-bar">
            <div 
              className={`timer-progress-fill ${timeRemaining <= 10 ? 'warning' : ''}`}
              style={{ width: `${(timeRemaining / 60) * 100}%` }}
            />
          </div>

          <div className="timer-text">
            <span className={timeRemaining <= 10 ? 'time-low' : ''}>
              {Math.ceil(timeRemaining)}s
            </span>
            <button 
              className="timer-toggle-btn"
              onClick={handleTimerToggle}
              title={isTimerRunning ? 'Pause timer' : 'Resume timer'}
            >
              {isTimerRunning ? '⏸' : '▶'}
            </button>
          </div>
        </div>

        <div className="content-area fullscreen-content">
          <div 
            className="translation-display"
            style={{ fontSize: `${questionFontSize}vh` }}
          >
            {currentWord.translation}
          </div>
       
          <div 
            className={`word-display ${isRevealed ? 'visible' : 'hidden'}`}
            style={{ fontSize: `${answerFontSize}vh` }}
          >
            {isRevealed ? currentWord.word : '❓'}
          </div>

          <div 
            className={`description word-display ${isRevealed ? 'visible' : 'hidden'}`}
            style={{ fontSize: `${questionFontSize - 1}vh` }}
          >
            {currentWord.description}
          </div>            
        </div>

        <div className="controls-hint fullscreen-hint">
          <div className="hint">
            Press <kbd>Space</kbd> or <kbd>Enter</kbd> to interact
          </div>
          <div className="hint font-controls">
            <span>Font size: </span>
            <button 
              className="font-btn" 
              onClick={() => {
                setAnswerFontSize(prev => Math.max(prev - 0.5, 2));
                setQuestionFontSize(prev => Math.max(prev - 0.5, 2));
              }}
            >
              A-
            </button>
            <button 
              className="font-btn" 
              onClick={() => {
                setAnswerFontSize(prev => Math.min(prev + 0.5, 15));
                setQuestionFontSize(prev => Math.min(prev + 0.5, 15));
              }}
            >
              A+
            </button>
            <span className="font-size-label">
              {(!isRevealed ? questionFontSize : answerFontSize).toFixed(1)}vh
            </span>
            <span className="font-target">
              ({!isRevealed ? 'Question' : 'Answer'})
            </span>
          </div>
          <div className="progress fullscreen-progress">
            {currentPosition} / {total} words
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
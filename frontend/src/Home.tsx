import React, { useEffect, useState } from 'react';
import { useTrainer } from './hooks/useTrainer';
import { useAuth } from './context/AuthContext';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';

import './Home.scss';

const Home: React.FC = () => {
  const [searchParams] = useSearchParams();
  const categoryId = searchParams.get('category_id');
  const categoryIdInt = categoryId ? parseInt(categoryId) : null;
  console.log('categoryId: ', categoryId, categoryIdInt);

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
  } = useTrainer(categoryIdInt);
  
  const { user, logout } = useAuth();

  // Font size states
  const [questionFontSize, setQuestionFontSize] = useState(6); // vw units
  const [answerFontSize, setAnswerFontSize] = useState(6);
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
        if (!isRevealed && words.length > 0 && currentWord) {
          revealWord();
        } else if (isRevealed && words.length > 0) {
          nextWord();
        }
      }
      // Font size controls (in vw)
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

  // Loading state - Full Screen
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

  // Error state - Full Screen
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

  // Completion state - Full Screen
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

  // No words state - Full Screen
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

  // Main app - Full Screen
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
              <button className="btn fullscreen-btn" onClick={revealWord}>
                Show Word
              </button>
            ) : (
              <button className="btn fullscreen-btn" onClick={nextWord}>
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
        <div className="progress fullscreen-progress">
          {currentPosition} / {total} words
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
          <div className="hint">
            <kbd>Shift</kbd> + <kbd>↑</kbd> / <kbd>↓</kbd> to adjust
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
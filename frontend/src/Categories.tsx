import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import categoryService from './services/categoryService';
import './Categories.scss';
import { Category } from './types';

const Categories: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await categoryService.fetchCategories();
        setCategories(data);
      } catch (err: any) {
        console.error('Error fetching categories:', err);
        setError(err.message || 'Failed to load categories');
        
        // If unauthorized, redirect to login
        if (err.status === 401) {
          navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, [navigate]);

  const handleCategoryClick = (categoryId: number) => {
    navigate(`/?category_id=${categoryId}`);
  };

  const handleAllWordsClick = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="categories-container">
        <h1>📚 Categories</h1>
        <div className="loading">Loading categories...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="categories-container">
        <h1>📚 Categories</h1>
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="categories-container">
      <h1>📚 Categories</h1>

    <div className="import-link-wrapper">
      <Link to="/upload">Import Category</Link>
    </div>
      
      <div className="categories-grid">
        {/* All words option */}
        <div 
          className="category-card all-words"
          onClick={handleAllWordsClick}
        >
          <div className="category-icon">📖</div>
          <h3>All Words</h3>
          <p className="word-count">
            {categories.reduce((sum, cat) => sum + (cat.word_count || 0), 0)} words
          </p>
        </div>

        {/* Individual categories */}
        {categories.map((category) => (
          <div 
            key={category.id}
            className="category-card"
            onClick={() => handleCategoryClick(category.id)}
          >
            <div className="category-icon">📂</div>
            <h3>{category.name}</h3>
            <p className="word-count">{category.word_count || 0} words</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Categories;
import React from 'react';
import './LoadingSpinner.scss';

export const LoadingSpinner: React.FC = () => {
    return (
        <div className="spinner-container">
            <div className="spinner"></div>
            <p>Loading...</p>
        </div>
    );
};
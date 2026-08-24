import React from 'react';
import { useAuth } from '../context/AuthContext';
import './Dashboard.scss';

export const Dashboard: React.FC = () => {
    const { user } = useAuth();

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <h1>Dashboard</h1>
                <p>Welcome back, {user?.first_name || user?.email}!</p>
            </div>
            
            <div className="dashboard-grid">
                <div className="card">
                    <h3>👤 Profile Information</h3>
                    <div className="info-item">
                        <span className="label">Email:</span>
                        <span className="value">{user?.email}</span>
                    </div>
                    <div className="info-item">
                        <span className="label">Username:</span>
                        <span className="value">{user?.username || 'Not set'}</span>
                    </div>
                    <div className="info-item">
                        <span className="label">Full Name:</span>
                        <span className="value">
                            {user?.first_name} {user?.last_name}
                        </span>
                    </div>
                    <div className="info-item">
                        <span className="label">Email Verified:</span>
                        <span className={`value ${user?.is_verified ? 'verified' : 'unverified'}`}>
                            {user?.is_verified ? '✅ Yes' : '❌ No'}
                        </span>
                    </div>
                </div>

                <div className="card">
                    <h3>📊 Quick Stats</h3>
                    <div className="stats-grid">
                        <div className="stat-item">
                            <span className="stat-value">0</span>
                            <span className="stat-label">Videos Generated</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-value">0</span>
                            <span className="stat-label">Projects</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-value">0</span>
                            <span className="stat-label">Templates</span>
                        </div>
                    </div>
                </div>

                <div className="card">
                    <h3>🚀 Quick Actions</h3>
                    <div className="action-buttons">
                        <button className="action-btn primary">Create New Video</button>
                        <button className="action-btn secondary">View Templates</button>
                        <button className="action-btn tertiary">Edit Profile</button>
                    </div>
                </div>
            </div>
        </div>
    );
};
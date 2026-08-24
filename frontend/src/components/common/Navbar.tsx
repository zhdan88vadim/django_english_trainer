import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Navbar.scss';

export const Navbar: React.FC = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <div className="navbar-brand">
                    <Link to="/">Video Generator</Link>
                </div>

                <div className="navbar-menu">
                    {user ? (
                        <>
                            <Link to="/dashboard" className="nav-link">Dashboard</Link>
                            <Link to="/profile" className="nav-link">Profile</Link>
                            <div className="nav-user">
                                <span className="user-email">{user.email}</span>
                                <button onClick={handleLogout} className="logout-btn">
                                    Logout
                                </button>
                            </div>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="nav-link">Login</Link>
                            <Link to="/register" className="nav-link register-btn">
                                Register
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};
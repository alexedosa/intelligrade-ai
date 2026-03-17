import React from 'react';
import './ProtectedRoute.css';

const ProtectedRoute = ({ children }) => {
    return (
        <div className="protected-route">
            {children}
        </div>
    );
};

export default ProtectedRoute;

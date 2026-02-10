import React from 'react';
import { useHistory } from 'react-router-dom';

const BackButton: React.FC = () => {
    const history = useHistory();

    return (
        <button
            onClick={() => history.goBack()}
            style={{
                backgroundColor: '#800000', // burgundy color
                color: '#FFFFFF',
                border: 'none',
                padding: '10px 20px',
                borderRadius: '5px',
                cursor: 'pointer'
            }}
        >
            Back
        </button>
    );
};

export default BackButton;
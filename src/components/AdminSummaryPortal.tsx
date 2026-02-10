import React, { useState } from 'react';

const AdminSummaryPortal = () => {
    const [totalSchools, setTotalSchools] = useState(0);
    const [activities, setActivities] = useState({ lecs: 0, gms: 0, communityDays: 0 });
    const [newActivity, setNewActivity] = useState('');

    const addActivity = () => {
        if (newActivity && activities[newActivity] !== undefined) {
            setActivities({ ...activities, [newActivity]: activities[newActivity] + 1 });
            setNewActivity('');
        }
    };

    return (
        <div>
            <h1>Admin Summary Dashboard</h1>
            <div>
                <h2>Total Schools: {totalSchools}</h2>
                <h2>Activities</h2>
                <ul>
                    <li>Lecs: {activities.lecs}</li>
                    <li>GMs: {activities.gms}</li>
                    <li>Community Days: {activities.communityDays}</li>
                </ul>
            </div>
            <div>
                <input 
                    type="text" 
                    value={newActivity} 
                    onChange={(e) => setNewActivity(e.target.value)} 
                    placeholder="Add Activity (lecs, gms, communityDays)" 
                />
                <button onClick={addActivity}>Add Activity</button>
            </div>
        </div>
    );
};

export default AdminSummaryPortal;
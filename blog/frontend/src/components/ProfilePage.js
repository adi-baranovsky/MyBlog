import { useEffect, useState } from "react";
import "../styles/ProfilePage.css"; // Import the CSS file

function ProfilePage() {
    const [profile, setProfile] = useState(null);
    const params = new URLSearchParams(window.location.search);
    const username = params.get("user");

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/profile/?user=${username}`)
            .then(res => res.json())
            .then(data => setProfile(data))
            .catch(err => console.error("Error loading profile:", err));
    }, [username]);

    if (!profile) return <p>Loading...</p>;

    return (
        <div className="profile-container">
            <div className="profile-header">
                <img src={profile.profile_image} alt="Profile" className="profile-image" />
                <div className="profile-info">
                    <h1 className="profile-username">{profile.username}</h1>
                    <p className="profile-bio">{profile.bio}</p>
                </div>
            </div>
        </div>
    );
    
}

export default ProfilePage;

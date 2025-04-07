import { useEffect, useState } from "react";

function ProfilePage() {
    const [profile, setProfile] = useState(null);
    const params = new URLSearchParams(window.location.search);
    const username = params.get("user"); // לוקח את שם המשתמש מה-URL

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/profile/?user=${username}`)
            .then(res => res.json())
            .then(data => setProfile(data))
            .catch(err => console.error("Error loading profile:", err));
    }, [username]);

    if (!profile) return <p>Loading...</p>;
    

    return (
        <div>
            <h1>{profile.username}'s Profile</h1>
            <img src={profile.profile_image} alt="Profile" style={{ width: "150px", height: "150px", borderRadius: "50%" }} />
            <p>{profile.bio}</p>
        </div>
    );
}

export default ProfilePage;

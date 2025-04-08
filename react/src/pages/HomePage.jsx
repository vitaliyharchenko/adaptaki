import React, { useEffect, useState } from "react";
import axios from "axios";

const HomePage = () => {
    const [username, setUsername] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem("access");
        axios
            .get("http://localhost:8000/api/users/me/", {
                headers: { Authorization: `Bearer ${token}` },
            })
            .then((res) => setUsername(res.data.username))
            .catch(() => setUsername("Гость"));
    }, []);

    return (
        <div style={{ padding: "2rem" }}>
            <h1>Панель методиста</h1>
            <p>Привет, {username || "..."}</p>
        </div>
    );
};

export default HomePage;

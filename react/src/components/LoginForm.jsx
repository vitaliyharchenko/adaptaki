import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const LoginForm = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(
                "http://localhost:8000/api/token/",
                {
                    username,
                    password,
                }
            );
            localStorage.setItem("access", response.data.access);
            localStorage.setItem("refresh", response.data.refresh);
            navigate("/");
        } catch (err) {
            setError("Неверный логин или ошибка запроса");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Логин"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit">Войти</button>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </form>
    );
};

export default LoginForm;

import React, { useEffect, useState } from "react";
import axios from "axios";
import LogoutButton from "../components/LogoutButton";

const HomePage = () => {
    const [username, setUsername] = useState(null);
    const [randomQuestion, setRandomQuestion] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem("access");
        axios
            .get("http://localhost:8000/api/users/me/", {
                headers: { Authorization: `Bearer ${token}` },
            })
            .then((res) => setUsername(res.data.first_name))
            .catch(() => setUsername("Гость"));

        axios
            .get("http://localhost:8000/api/questions/random/", {
                headers: { Authorization: `Bearer ${token}` },
            })
            .then((res) => setRandomQuestion(res.data))
            .catch(() =>
                setRandomQuestion("ошибка при получении случайного вопроса")
            );
    }, []);

    return (
        <div style={{ padding: "2rem" }}>
            <h1>Панель методиста</h1>
            <p>Привет, {username || "..."}</p>
            <p>
                Случайный вопрос:{" "}
                {randomQuestion ? randomQuestion.question_text_new : "..."}
            </p>
            <LogoutButton />
        </div>
    );
};

export default HomePage;

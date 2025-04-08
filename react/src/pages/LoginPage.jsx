import React from "react";
import LoginForm from "../components/LoginForm";

const LoginPage = () => {
    return (
        <div style={{ maxWidth: 400, margin: "50px auto" }}>
            <h2>Авторизация</h2>
            <LoginForm />
        </div>
    );
};

export default LoginPage;

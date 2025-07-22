import React, {useEffect, useState} from "react";
import httpClient from "../httpClient";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/authContext";

const LoginPage = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const { user, fetchUser } = useAuth();

    useEffect(() => {
        if (user) {
            console.log("User logged in, navigating to dashboard");
            navigate("/dashboard", { replace: true });
        }
    }, [user, navigate]);

    const logInUser = async () => {
        try {
            await httpClient.post("http://localhost:5000/login", {
                email,
                password,
            });

            await fetchUser(); // 🚀 Update user state
            navigate("/dashboard");     // Route without reload
        } catch (error) {
            if (error.response?.status === 401) {
                alert("Invalid credentials");
            }
        }
    };

    return (
        <div>
            <h1>Login to your account</h1>
            <form>
                <div>
                    <label>Email</label>
                    <input
                        type="text"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div>
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="button" onClick={logInUser}>Submit</button>
            </form>
        </div>
    );
};

export default LoginPage;

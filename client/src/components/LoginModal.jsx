import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {useAuth} from "../contexts/authContext.jsx";
import httpClient from "../httpClient.js";
import {useSetAtom} from "jotai";
import uiAtom from "./state.jsx";

function LoginModal() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const { fetchUser } = useAuth();
    const setUi = useSetAtom(uiAtom)

    // useEffect(() => {
    //     if (user) {
    //         console.log("User logged in, navigating to dashboard");
    //         navigate("/dashboard", { replace: true });
    //     }
    // }, [user, navigate]);

    const logInUser = async () => {
        try {
            await httpClient.post("http://localhost:5000/login", {
                email,
                password,
            });

            await fetchUser();
            setUi((prev) => ({ ...prev, modal: null }))
            navigate("/dashboard");
        } catch (error) {
            if (error.response?.status === 401) {
                alert("Invalid credentials");
            }
        }
    };

    return <div className="login-modal">
        <div className="login-content">

            <button id="close-btn" onClick={() => {
                setUi((prev) => ({
                    ...prev,
                    modal: false,
                }))
            }}>X
            </button>

            <form>
                <div id={"log-register"}>
                    <label>Email</label>
                    <input type="text" value={email}
                           onChange={(e) => setEmail(e.target.value)}/>
                </div>

                <div id={"log-register"}>
                    <label>Password</label>
                    <input type="password" value={password}
                           onChange={(e) => setPassword(e.target.value)}/>
                </div>

                <button type="button" onClick={logInUser}>Login</button>

            </form>
        </div>

    </div>

}

export default LoginModal
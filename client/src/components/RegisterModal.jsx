import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {useAuth} from "../contexts/authContext.jsx";
import httpClient from "../httpClient.js";
import {useSetAtom} from "jotai";
import uiAtom from "./state.jsx";

function RegisterModal() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const { user } = useAuth();
    const setUi = useSetAtom(uiAtom)

    useEffect(() => {
        if (user) {
            navigate("/dashboard", {replace: true});
        }
    }, [user, navigate]);

    const registerUser = async () => {

        const resp = await httpClient.post("//localhost:5000/register", {
            email,
            password,
        });
        setUi((prev) => ({ ...prev, modal: null }))
    }

    return (
        <div className={"register-modal"}>
            <div className={"register-content"}>

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
                        <input
                            type="text"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            id=""
                        />
                    </div>
                    <div id={"log-register"}>
                        <label>Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            id=""
                        />
                    </div>
                    <button type="button" onClick={() => registerUser()}>Register</button>
                </form>
            </div>

        </div>
    )
}

export default RegisterModal
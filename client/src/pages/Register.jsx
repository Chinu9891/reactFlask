import React, {useEffect, useState} from "react"
import httpClient from "../httpClient"
import { useNavigate } from "react-router-dom";
import {useAuth} from "../contexts/authContext.jsx";

const RegisterPage = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const { user } = useAuth();

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
        navigate('/')
    }

    return (
        <div className={"register-container"}>
            <h1>Register an account</h1>
            <form>
                <div>
                    <label>Email</label>
                    <input
                        type="text"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        id=""
                    />
                </div>
                <div>
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        id=""
                    />
                </div>
                <button type="button" onClick={() => registerUser()}>Submit</button>
            </form>
        </div>
    )
}

export default RegisterPage
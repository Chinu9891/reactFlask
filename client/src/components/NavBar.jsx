import {Link} from "react-router-dom";
import "./navbar.css"
import React from "react";
import httpClient from "../httpClient.js";
import { useNavigate } from "react-router-dom";
import {useAuth} from "../contexts/authContext.jsx";
import { useLocation } from "react-router-dom";

function NavBar() {
    const navigate = useNavigate();
    const { fetchUser } = useAuth();
    const location = useLocation();

    const handleLogout = async () => {
        await httpClient.post("http://localhost:5000/logout");
        await fetchUser();
        navigate('/')
    };

    return <nav className="nav">
        <Link to="/dashboard" className="site-title">Streamer Notifier</Link>
        <ul>
            <li>
                {location.pathname === "/favorites" ? (
                    <Link to="/dashboard">Dashboard</Link>
                ) : (
                    <Link to="/favorites">Subscriptions</Link>
                )}
            </li>
            <li>
                <button onClick={handleLogout}>Logout</button>
            </li>
        </ul>
    </nav>
}

export default NavBar
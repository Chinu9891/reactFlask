import {Link} from "react-router-dom";
import "./navbar.css"
import React from "react";
import httpClient from "../httpClient.js";
import { useNavigate } from "react-router-dom";
import {useAuth} from "../contexts/authContext.jsx";

function NavBar() {
    const navigate = useNavigate();
    const { fetchUser } = useAuth();

    const handleLogout = async () => {
        await httpClient.post("http://localhost:5000/logout");
        await fetchUser();
        navigate('/')
    };

    return <nav className="nav">
        <Link to="/dashboard" className="site-title">Streamer Notifier</Link>
        <ul>
            <li>
                <Link to="/favorites">Favorites</Link>
            </li>
            <li>
                <button onClick={handleLogout}>Logout</button>
            </li>
        </ul>
    </nav>
}

export default NavBar
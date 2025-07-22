import "./border.css"
import { useAuth } from "../contexts/authContext.jsx";
import {Link, useNavigate} from "react-router-dom";
import { useEffect } from "react";

const LandingPage = () => {
    const { user } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (user) {
            console.log("huh")
            navigate("/dashboard");
        }
    }, [user, navigate]);

    return (
        <div className="landing-container">
            <div className="landing-left">
                <h1>Twitch notifier</h1>
            </div>
            <div className="landing-divider"></div>
            <div className="landing-right">
                {!user && (
                <>
                    <h1>Login to access the dashboard</h1>
                    <div>
                        <Link to="/login">
                            <button className="login-span">Login</button>
                        </Link>

                        <Link to="/register">
                            <button className="login-span">Register</button>
                        </Link>
                    </div>
                </>
            )}
            </div>
        </div>
    );
};

export default LandingPage;

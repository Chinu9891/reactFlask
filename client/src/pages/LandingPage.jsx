import "./landing_page.css"
import { useAuth } from "../contexts/authContext.jsx";
import {Link, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import Overlays from "../components/Overlays.jsx";
import {useSetAtom} from "jotai";
import uiAtom from "../components/state.jsx";
import LoginModal from "../components/LoginModal.jsx";
import RegisterModal from "../components/RegisterModal.jsx";

const LandingPage = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const setUi = useSetAtom(uiAtom)

    const [currModal, setModal] = useState(null)


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
            <div className="landing-divider">

            </div>
            <div className="landing-right">
                {!user && (
                    <>
                        <Overlays />
                        <h1>Login to access the dashboard</h1>
                        <div className="navigate-actions">
                            <button className="navigate-item" onClick={() => setUi(
                                (prev) => ({
                                    ...prev,
                                    modal: true,
                                    currModal: <LoginModal/>,
                                })
                            )}>Login
                            </button>

                            <button className="navigate-item" onClick={() => setUi(
                                (prev) => ({
                                    ...prev,
                                    modal: true,
                                    currModal: <RegisterModal/>
                                })
                            )}>Register
                            </button>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default LandingPage;

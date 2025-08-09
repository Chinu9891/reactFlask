import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage.jsx";
import Favorites from "./pages/Favorites.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import ProtectedRoute from "./components/ProtectedRoute";

const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route
                path="/favorites"
                element={
                    <ProtectedRoute>
                        <Favorites />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/dashboard"
                element={
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                }
            />
        </Routes>
    );
};

export default AppRoutes;

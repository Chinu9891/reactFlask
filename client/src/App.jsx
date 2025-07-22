import AppRoutes from "./AppRoutes.jsx";
import { AuthProvider } from "./contexts/authContext";

function App() {
    return (
        <AuthProvider>
            <AppRoutes />
        </AuthProvider>
    );
}

export default App;

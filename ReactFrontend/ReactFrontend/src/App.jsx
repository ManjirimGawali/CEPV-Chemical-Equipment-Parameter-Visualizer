import { Routes, Route, Navigate, BrowserRouter } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";

import ProtectedRoute from "./routes/ProtectedRoute";
import MainLayout from "./layouts/MainLayout";
import Testing from "./pages/Testing";

function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/testing" element={<Testing/>} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Dashboard />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/history"
        element={
          <ProtectedRoute>
            <MainLayout>
              <History />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      {/* Default */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>



    // <Routes>
    //   {/* Public */}
    //   <Route path="/login" element={<Login />} />
    //   <Route path="/signup" element={<Signup />} />

    //   {/* Protected */}
    //   <Route
    //     path="/dashboard"
    //     element={
    //       <ProtectedRoute>
    //         <MainLayout>
    //           <Dashboard />
    //         </MainLayout>
    //       </ProtectedRoute>
    //     }
    //   />

    //   <Route
    //     path="/history"
    //     element={
    //       <ProtectedRoute>
    //         <MainLayout>
    //           <History />
    //         </MainLayout>
    //       </ProtectedRoute>
    //     }
    //   />

    //   {/* Default */}
    //   <Route path="*" element={<Navigate to="/dashboard" replace />} />
    // </Routes>
  );
}

export default App;

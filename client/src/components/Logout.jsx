import auth from "../services/authService";
import { useEffect } from "react";

const Logout = () => {
  useEffect(() => {
    auth.logout();
    window.location = "/";
  }, []);
  return null;
};

export default Logout;

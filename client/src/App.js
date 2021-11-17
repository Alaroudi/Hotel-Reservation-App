import { Redirect, Route, Switch } from "react-router";
import PageNotFound from "./components/PageNotFound";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import Profile from "./components/Profile";
import Logout from "./components/Logout";
import NavBar from "./components/NavBar";
import Home from "./components/Home";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useEffect, useState } from "react";
import auth from "./services/authService";
import HotelsTable from "./components/HotelsTable";
import HotelForm from "./components/HotelForm";
import HotelSearch from "./components/HotelSearch";
import ProtectedRoute from "./components/common/protectedRoute";
import MyReservations from "./components/MyReservations";

const App = () => {
  const [user, setUser] = useState();

  useEffect(() => {
    const user = auth.getCurrentUser();
    setUser(user);
  }, []);

  return (
    <>
      <ToastContainer />
      <div className="app">
        <NavBar user={user} />
        <Switch>
          <Route path="/signin" component={SignIn} />
          <Route path="/signup" component={SignUp} />
          <ProtectedRoute path="/profile" component={Profile} />
          <Route path="/logout" component={Logout} />
          <Route path="/home" component={Home} />
          <ProtectedRoute path="/hotels/:id" component={HotelForm} />
          <ProtectedRoute path="/hotels" component={HotelsTable} />
          <Route path="/hotel-search" component={HotelSearch} />
          <ProtectedRoute path="/my-reservations" component={MyReservations} />
          <Route path="/not-found" component={PageNotFound} />
          <Redirect from="/" exact to="/home" />
          <Redirect to="/not-found" />
        </Switch>
      </div>
    </>
  );
};

export default App;

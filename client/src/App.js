import { Redirect, Route, Switch } from "react-router";
import PageNotFound from "./components/PageNotFound";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import NavBar from "./components/NavBar";
import Home from "./components/Home";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useEffect, useState } from "react";
import auth from "./services/authService";
import Logout from "./components/Logout";

const App = () => {
  const [user, setUser] = useState();

  useEffect(() => {
    const user = auth.getCurrentUser();
    console.log(user);
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
          <Route path="/logout" component={Logout} />
          <Route path="/home" component={Home} />
          <Route path="/not-found" component={PageNotFound} />
          <Redirect from="/" exact to="/home" />
          <Redirect to="/not-found" />
        </Switch>
      </div>
    </>
  );
};

export default App;

import { Redirect, Route, Switch } from "react-router";
import PageNotFound from "./components/PageNotFound";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import NavBar from "./components/NavBar";
import Home from "./components/Home";

const App = () => {
  return (
    <div className="app">
      <NavBar />

      <Switch>
        <Route path="/signin" component={SignIn} />
        <Route path="/signup" component={SignUp} />
        <Route path="/not-found" component={PageNotFound} />
        <Route path="/" exact component={Home} />
        <Redirect to="/not-found" />
      </Switch>
    </div>
  );
};

export default App;

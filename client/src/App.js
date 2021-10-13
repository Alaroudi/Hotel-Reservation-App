import { Redirect, Route, Switch } from "react-router";
import PageNotFound from "./components/PageNotFound";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";

function App() {
  return (
    <>
      <Switch>
        <Route path="/signin" component={SignIn} />
        <Route path="/signup" component={SignUp} />
        <Route path="/not-found" component={PageNotFound} />
        <Redirect to="/not-found" />
      </Switch>
    </>
  );
}

export default App;

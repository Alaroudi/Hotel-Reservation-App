import MenuIcon from "@mui/icons-material/Menu";
import IconButton from "@mui/material/IconButton";
import { useState } from "react";
import { Link, useHistory } from "react-router-dom";
import "./NavBar.css";

const NavBar = () => {
  const [toggle, setToggle] = useState(false);
  const history = useHistory();
  return (
    <nav className={toggle ? "nav collapsible--expanded" : "nav"}>
      <Link className="brand" to="/">
        <img src="/images/logo.svg" width="75px" alt="" />
        <span className="brand__name">Hotel Reservations</span>
      </Link>

      <IconButton className="nav__toggler" onClick={() => setToggle(!toggle)}>
        <MenuIcon />
      </IconButton>

      <ul className="list nav__list collapsible__content ">
        <li className="nav__item" onClick={() => history.push("/signin")}>
          Sign in
        </li>

        <li className="nav__item" onClick={() => history.push("/profile")}>
          Profile
        </li>
        <li className="nav__item" onClick={() => history.push("/reservations")}>
          My Reservations
        </li>

        <li className="nav__item" onClick={() => history.push("/admin")}>
          Admin
        </li>

        <li className="nav__item" onClick={() => history.push("/logout")}>
          Logout
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;

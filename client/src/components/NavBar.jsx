import MenuIcon from "@mui/icons-material/Menu";
import IconButton from "@mui/material/IconButton";
import { useState } from "react";
import { Link } from "react-router-dom";
import "./NavBar.css";
const NavBar = () => {
  const [toggle, setToggle] = useState(false);
  return (
    <nav className={toggle ? "nav collapsible--expanded" : "nav"}>
      <Link className="brand" to="/">
        <img src="./images/logo.svg" width="50px" alt="" />
        <span className="brand__name">Hotel Reservations</span>
      </Link>

      <IconButton className="nav__toggler" onClick={() => setToggle(!toggle)}>
        <MenuIcon />
      </IconButton>

      <ul className="list nav__list collapsible__content ">
        <li className="nav__item">
          <Link to="/signin">Sign in</Link>
        </li>
        <li className="nav__item">
          <Link to="/profile">Profile</Link>
        </li>
        <li className="nav__item">
          <Link to="#">Logout</Link>
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;

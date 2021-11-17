import MenuIcon from "@mui/icons-material/Menu";
import { Menu, MenuItem } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import { useState } from "react";
import { Link, useHistory } from "react-router-dom";
import "./NavBar.css";

const NavBar = ({ user }) => {
  const [toggle, setToggle] = useState(false);
  const history = useHistory();

  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const handleClick = event => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
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
        {!user && (
          <>
            <li className="nav__item" onClick={() => history.push("/signin")}>
              Sign in
            </li>
            <li className="nav__item" onClick={() => history.push("/signup")}>
              Register
            </li>
          </>
        )}
        {user && (
          <>
            <li className="nav__item" onClick={() => history.push("/profile")}>
              Profile
            </li>
            <li
              className="nav__item"
              onClick={() => history.push("/my-reservations")}
            >
              My Reservations
            </li>
            {user.isAdmin && (
              <>
                <li className="nav__item" onClick={handleClick}>
                  Admin
                </li>
                <Menu
                  id="basic-menu"
                  anchorEl={anchorEl}
                  open={open}
                  sx={{ color: "black" }}
                  onClose={handleClose}
                  MenuListProps={{
                    "aria-labelledby": "basic-button"
                  }}
                >
                  <MenuItem
                    onClick={() => {
                      handleClose();
                      history.push("/hotels");
                    }}
                  >
                    Hotels
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      handleClose();
                      history.push("/reservations");
                    }}
                  >
                    User Reservations
                  </MenuItem>
                </Menu>
              </>
            )}
            <li className="nav__item" onClick={() => history.push("/logout")}>
              Logout
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default NavBar;

import { useState } from "react";
import { Link } from "react-router-dom";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import InputAdornment from "@mui/material/InputAdornment";
import IconButton from "@mui/material/IconButton";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import LoginIcon from "@mui/icons-material/Login";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import LockIcon from "@mui/icons-material/Lock";
import "./SignIn.css";
const SignIn = () => {
  const [values, setValues] = useState({
    email: "",
    password: ""
  });
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = event => {
    setValues({ ...values, [event.target.id]: event.target.value });
  };

  // TODO: Call User API
  const handleSubmit = event => {
    event.preventDefault();
  };

  return (
    <div className="signin-container">
      <div className="form-container">
        <div style={{ width: "80%" }}>
          <Typography variant="h2" textAlign="center" mb={"100px"}>
            Sign in
          </Typography>
          <Box
            onSubmit={handleSubmit}
            component="form"
            sx={{
              display: "flex",
              flexDirection: "column",
              "& > :not(style)": { mb: 3 }
            }}
          >
            <TextField
              variant="outlined"
              label="Email"
              id="email"
              type="email"
              fullWidth
              required
              value={values.email}
              onChange={handleChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <AccountCircleIcon />
                  </InputAdornment>
                )
              }}
            />
            <TextField
              variant="outlined"
              label="Password"
              id="password"
              fullWidth
              required
              type={showPassword ? "text" : "password"}
              value={values.password}
              onChange={handleChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <LockIcon />
                  </InputAdornment>
                ),
                endAdornment: values.password && (
                  <InputAdornment position="end">
                    <IconButton onClick={() => setShowPassword(!showPassword)}>
                      {showPassword ? (
                        <VisibilityIcon />
                      ) : (
                        <VisibilityOffIcon />
                      )}
                    </IconButton>
                  </InputAdornment>
                )
              }}
            />
            <Link to="/signup" className="link">
              Create Account
            </Link>
            <Button
              variant="contained"
              type="submit"
              size="large"
              endIcon={<LoginIcon />}
              sx={{ borderRadius: "20px", mt: "1rem" }}
            >
              Sign in
            </Button>
          </Box>
        </div>
        <div>
          <img src="./images/login.svg" alt="" width="100%" />
        </div>
      </div>
    </div>
  );
};

export default SignIn;

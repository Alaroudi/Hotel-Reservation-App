import { useState } from "react";
import { Link } from "react-router-dom";
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
import auth from "../services/authService";
import Alert from "@mui/material/Alert";
import { Redirect } from "react-router";
import LoadingButton from "@mui/lab/LoadingButton";

const SignIn = ({ location }) => {
  const [values, setValues] = useState({
    email: "",
    password: ""
  });
  const [showPassword, setShowPassword] = useState(false);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = event => {
    setValues({ ...values, [event.target.id]: event.target.value });
  };

  // TODO: Call User API
  const handleSubmit = async event => {
    event.preventDefault();
    setLoading(false);
    setError("");
    try {
      setLoading(true);
      await auth.login(values.email, values.password);
      console.log(`${location.state.from.pathname}${location.state.search}`);
      window.location = location.state
        ? `${location.state.from.pathname}${location.state.from.search}`
        : "/";
    } catch (ex) {
      if (ex.response && ex.response.status === 400) {
        setError(ex.response.data);
      }
    }
    setLoading(false);
  };

  if (auth.getCurrentUser()) return <Redirect to="/" />;

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
            {error && (
              <Alert className="grid-span" severity="error">
                {error}
              </Alert>
            )}
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
            <LoadingButton
              variant="contained"
              type="submit"
              size="large"
              loading={loading}
              loadingPosition="end"
              endIcon={<LoginIcon />}
              sx={{ borderRadius: "20px", mt: "1rem" }}
            >
              Sign in
            </LoadingButton>
          </Box>
        </div>
        <div>
          <img src="/images/login.svg" alt="" width="100%" />
        </div>
      </div>
    </div>
  );
};

export default SignIn;

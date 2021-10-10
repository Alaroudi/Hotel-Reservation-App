import { useState } from "react";
import {
  Button,
  Container,
  TextField,
  Typography,
  Box,
  InputAdornment,
  IconButton
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import LoginIcon from "@mui/icons-material/Login";
import { Link } from "react-router-dom";

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
    <Container
      maxWidth="sm"
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        height: "100vh"
      }}
    >
      <Typography variant="h2" textAlign="center" mb={"100px"}>
        Sign in
      </Typography>
      <Box
        onSubmit={handleSubmit}
        component="form"
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",

          "& > :not(style)": { mb: 3, width: "80%" }
        }}
      >
        <TextField
          variant="outlined"
          label="Email"
          id="email"
          type="email"
          required
          value={values.email}
          onChange={handleChange}
        />
        <TextField
          variant="outlined"
          label="Password"
          id="password"
          type={showPassword ? "text" : "password"}
          required
          value={values.password}
          onChange={handleChange}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton onClick={() => setShowPassword(!showPassword)}>
                  {showPassword ? <VisibilityIcon /> : <VisibilityOffIcon />}
                </IconButton>
              </InputAdornment>
            )
          }}
        />

        <Link to="/signup" style={{ textDecoration: "none", fontSize: "1rem" }}>
          Create Account
        </Link>

        <Button
          variant="contained"
          type="submit"
          size="large"
          endIcon={<LoginIcon />}
          sx={{ borderRadius: "20px" }}
        >
          Sign in
        </Button>
      </Box>
    </Container>
  );
};

export default SignIn;

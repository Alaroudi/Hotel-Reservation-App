import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import { useState } from "react";
import { DatePicker, LocalizationProvider } from "@mui/lab";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import "./SignUp.css";
import { Link, Redirect } from "react-router-dom";
import * as userService from "../services/userService";
import auth from "../services/authService";
import LoadingButton from "@mui/lab/LoadingButton";

const SignUp = () => {
  const [user, setUser] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    phone_number: "",
    date_of_birth: null
  });

  const [error, setError] = useState({
    password: false,
    confirmPassword: false,
    email: ""
  });

  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = event => {
    if (event.target.id === "password" && event.target.value.length < 4) {
      setError({ ...error, password: true });
    } else {
      setError({ ...error, password: false });
    }
    setUser({ ...user, [event.target.id]: event.target.value });
  };

  const handleSubmit = async event => {
    event.preventDefault();
    if (error.password || error.confirmPassword) return;
    setError({ ...error, email: "" });
    setSuccess(false);
    setLoading(false);

    try {
      setLoading(true);
      await userService.register(user);
      setSuccess(true);
    } catch (ex) {
      if (ex.response && ex.response.status === 400) {
        setError({ ...error, email: ex.response.data });
      }
    }
    setLoading(false);
  };

  if (auth.getCurrentUser()) return <Redirect to="/" />;

  return (
    <Container
      component="form"
      onSubmit={handleSubmit}
      maxWidth="sm"
      sx={{
        height: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "0"
      }}
    >
      <div className="grid">
        <Typography
          variant="h4"
          mb={"3rem"}
          textAlign="center"
          className="grid-span"
        >
          Create Your Account
        </Typography>
        {error.email && (
          <Alert className="grid-span" severity="error">
            {error.email}
          </Alert>
        )}
        {success && (
          <Alert
            className="grid-span"
            sx={{ textAlign: "center" }}
            severity="success"
          >
            Account Created!
          </Alert>
        )}
        <TextField
          variant="outlined"
          label="First name"
          required
          id="first_name"
          onChange={handleChange}
        />
        <TextField
          variant="outlined"
          label="Last name"
          required
          id="last_name"
          onChange={handleChange}
        />
        <TextField
          variant="outlined"
          label="Email"
          type="email"
          fullWidth
          required
          id="email"
          onChange={handleChange}
          className="grid-span"
        />

        <TextField
          variant="outlined"
          label="Password"
          type="password"
          required
          id="password"
          error={error.password}
          helperText={
            error.password ? "Must be at least 4 characters long" : ""
          }
          onChange={handleChange}
        />
        <TextField
          variant="outlined"
          label="Confirm"
          type="password"
          required
          error={error.confirmPassword}
          helperText={error.confirmPassword ? "Passwords Don't Match" : ""}
          onChange={event =>
            event.target.value !== user.password
              ? setError({ ...error, confirmPassword: true })
              : setError({ ...error, confirmPassword: false })
          }
        />
        <TextField
          variant="outlined"
          label="Phone number"
          type="text"
          id="phone_number"
          onChange={handleChange}
        />
        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <DatePicker
            label="Date of Birth"
            value={user.date_of_birth}
            required
            onChange={newValue => {
              setUser({ ...user, date_of_birth: newValue });
            }}
            renderInput={params => <TextField required {...params} />}
          />
        </LocalizationProvider>

        <Link to="/signin" className="link">
          Sign in instead
        </Link>
        <LoadingButton
          variant="contained"
          type="submit"
          size="large"
          loading={loading}
          loadingPosition="end"
          sx={{ borderRadius: "20px", mt: 3 }}
          className="grid-span"
          endIcon={<PersonAddIcon />}
        >
          Register
        </LoadingButton>
      </div>
    </Container>
  );
};

export default SignUp;

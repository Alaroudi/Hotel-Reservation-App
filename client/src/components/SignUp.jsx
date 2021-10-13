import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { useState } from "react";
import { DatePicker, LocalizationProvider } from "@mui/lab";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import "./SignUp.css";
import { Link } from "react-router-dom";

const SignUp = () => {
  const [values, setValues] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    phone_number: "",
    date_of_birth: null
  });

  const [error, setError] = useState({
    password: false,
    confirmPassword: false
  });

  const handleChange = event => {
    if (event.target.id === "password" && event.target.value.length < 8) {
      setError({ ...error, password: true });
    } else {
      setError({ ...error, password: false });
    }
    setValues({ ...values, [event.target.id]: event.target.value });
  };

  const handleSubmit = event => {
    event.preventDefault();

    if (error.password || error.confirmPassword) return;
    console.log(values);
  };
  return (
    <Container
      component="form"
      onSubmit={handleSubmit}
      maxWidth="sm"
      sx={{
        height: "100vh",
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
            error.password ? "Must be at least 8 characters long" : ""
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
            event.target.value !== values.password
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
            value={values.date_of_birth}
            required
            onChange={newValue => {
              setValues({ ...values, date_of_birth: newValue });
            }}
            renderInput={params => <TextField required {...params} />}
          />
        </LocalizationProvider>

        <Link to="/signin" className="link">
          Sign in instead
        </Link>
        <Button
          variant="contained"
          type="submit"
          size="large"
          sx={{ borderRadius: "20px", mt: 3 }}
          className="grid-span"
          endIcon={<PersonAddIcon />}
        >
          Sign up
        </Button>
      </div>
    </Container>
  );
};

export default SignUp;

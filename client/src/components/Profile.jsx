import React from "react";
import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import { useState, useEffect } from "react";
import { DatePicker, LocalizationProvider } from "@mui/lab";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import LoadingButton from "@mui/lab/LoadingButton";
import EditIcon from "@mui/icons-material/Edit";
import IconButton from "@mui/material/IconButton";
import "./Profile.css";
import * as userService from "../services/userService";
import auth from "../services/authService";

const Profile = () => {
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
  const [buttonLoading, setButtonLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [disapled, setDisapled] = useState(true);

  useEffect(() => {
    setLoading(true);
    const getUser = async () => {
      const user_id = auth.getCurrentUser()?.id;
      const userInfo = await userService.getUser(user_id);
      setUser(userInfo.data);
      setLoading(false);
      //   console.log(userInfo.data);
    };
    getUser();
  }, []);

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
    setButtonLoading(false);
    try {
      setButtonLoading(true);
      const user_id = auth.getCurrentUser()?.id;
      await userService.editUser(user_id, user);
      setSuccess(true);
    } catch (ex) {
      if (ex.response && ex.response.status === 400) {
        setError({ ...error, email: ex.response.data });
      }
    }
    setButtonLoading(false);
    setDisapled(true);
  };

  if (loading) {
    return <h1>Loading...</h1>;
  }

  return (
    <Container
      component="form"
      onSubmit={handleSubmit}
      maxWidth="md"
      sx={{
        height: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "0"
      }}
    >
      <div className="profile-grid">
        <Typography variant="h4" className="grid-span profile-typography">
          User Profile
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
            Account Updated!
          </Alert>
        )}
        <IconButton
          color="success"
          className="grid-span edit-icon"
          onClick={() => {
            setDisapled(!disapled);
            setSuccess(false);
          }}
        >
          Edit
          <EditIcon />
        </IconButton>
        <TextField
          variant="outlined"
          label="First name"
          id="first_name"
          onChange={handleChange}
          disabled={disapled}
          defaultValue={user.first_name}
        />
        <TextField
          variant="outlined"
          label="Last name"
          id="last_name"
          defaultValue={user.last_name}
          onChange={handleChange}
          disabled={disapled}
        />
        <TextField
          variant="outlined"
          label="Email"
          type="email"
          fullWidth
          id="email"
          defaultValue={user.email}
          onChange={handleChange}
          className="grid-span"
          disabled={disapled}
        />

        <TextField
          variant="outlined"
          label="Password"
          type="password"
          disabled={disapled}
          id="password"
          defaultValue={user.password}
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
          defaultValue={user.password}
          disabled={disapled}
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
          disabled={disapled}
          defaultValue={user.phone_number}
          onChange={handleChange}
        />
        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <DatePicker
            label="Date of Birth"
            value={user.date_of_birth}
            onChange={newValue => {
              setUser({ ...user, date_of_birth: newValue });
            }}
            disabled={disapled}
            renderInput={params => <TextField {...params} />}
          />
        </LocalizationProvider>

        <LoadingButton
          variant="contained"
          type="submit"
          size="large"
          disabled={disapled}
          loading={buttonLoading}
          loadingPosition="end"
          sx={{ borderRadius: "20px", mt: 3 }}
          className="grid-span"
          endIcon={<AccountCircleIcon />}
        >
          Update
        </LoadingButton>
      </div>
    </Container>
  );
};

export default Profile;

import "./Hotels.css";
import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import FormLabel from "@mui/material/FormLabel";
import Alert from "@mui/material/Alert";
import LoadingButton from "@mui/lab/LoadingButton";
import EditIcon from "@mui/icons-material/Edit";
import { useState, useEffect } from "react";
import "./Profile.css";
import * as hotelService from "../services/hotelService";
import Loading from "./common/Loading";
import HotelIcon from "@mui/icons-material/Hotel";
import InputAdornment from "@mui/material/InputAdornment";
import Checkbox from "@mui/material/Checkbox";
import FormControl from "@mui/material/FormControl";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormGroup from "@mui/material/FormGroup";
import Button from "@mui/material/Button";
import { getCurrentUser } from "../services/authService";
const user = getCurrentUser();
const HotelForm = ({ match, history }) => {
  const [hotel, setHotel] = useState({
    hotel_name: "",
    street_address: "",
    city: "",
    state: "",
    zipcode: "",
    phone_number: "",
    weekend_diff_percentage: 0.0,
    Spa: false,
    Pool: false,
    Gym: false,
    Bussiness_Office: false,
    Wifi: false,
    king_count: 0,
    king_price: 0.0,
    queen_count: 0,
    queen_price: 0.0,
    standard_count: 0,
    standard_price: 0.0
  });

  const [error, setError] = useState("");

  const [success, setSuccess] = useState(false);
  const [buttonLoading, setButtonLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [disapled, setDisapled] = useState(true);
  const [showEdit, setShowEdit] = useState(true);

  useEffect(() => {
    const getHotel = async () => {
      const hotelId = match.params.id;
      if (hotelId === "new") {
        setLoading(false);
        setDisapled(false);
        setShowEdit(false);
        return;
      }

      try {
        const { data: hotelInfo } = await hotelService.getHotel(hotelId);
        const { amenities } = hotelInfo;
        if (amenities.length > 0) {
          if (amenities.includes("Pool")) {
            hotelInfo.Pool = true;
          }
          if (amenities.includes("Gym")) hotelInfo.Gym = true;
          if (amenities.includes("Spa")) hotelInfo.Spa = true;
          if (amenities.includes("Business Office"))
            hotelInfo.Bussiness_Office = true;
          if (amenities.includes("Wifi")) hotelInfo.Wifi = true;
        }
        delete hotelInfo.amenities;
        setHotel(h => {
          return { ...h, ...hotelInfo };
        });
      } catch (ex) {
        if (ex.response) {
          if (ex.response.status === 404) history.replace("/not-found");
          if (ex.response.status === 400) {
            setError(ex.response.data.message);
          }
        }
      } finally {
        setLoading(false);
      }
    };

    getHotel();
  }, [history, match]);

  const handleChange = event => {
    if (event.target.id === "weekend_diff_percentage") {
      setHotel({ ...hotel, [event.target.id]: event.target.value / 100 });
      return;
    }
    setHotel({ ...hotel, [event.target.id]: event.target.value });
  };

  const handleSubmit = async event => {
    event.preventDefault();
    setError("");
    setSuccess(false);
    setButtonLoading(false);
    try {
      setButtonLoading(true);
      await hotelService.saveHotel(hotel);
      setSuccess(true);
      setDisapled(true);
    } catch (ex) {
      if (ex.response) {
        if (ex.response.status === 400) {
          setError(ex.response.data.message);
        }
      }
      setDisapled(false);
    } finally {
      setButtonLoading(false);
    }
  };

  if (loading) {
    return <Loading />;
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
      <div className="hotel-grid">
        <Typography
          variant="h4"
          className="grid-span"
          mb="2rem"
          textAlign="center"
        >
          Hotel Information
        </Typography>
        {error && (
          <Alert className="grid-span" severity="error">
            {error}
          </Alert>
        )}
        {success && (
          <Alert
            className="grid-span"
            sx={{ textAlign: "center" }}
            severity="success"
          >
            Hotel Info Saved!
          </Alert>
        )}
        {showEdit && user.isAdmin && (
          <Button
            color="secondary"
            className="edit-btn"
            size="large"
            endIcon={<EditIcon />}
            onClick={() => {
              setDisapled(!disapled);
              setSuccess(false);
            }}
          >
            Edit
          </Button>
        )}

        <TextField
          variant="outlined"
          label="Hotel name"
          className="grid-span"
          id="hotel_name"
          onChange={handleChange}
          disabled={disapled}
          defaultValue={hotel.hotel_name}
          required
        />
        <TextField
          variant="outlined"
          label="Street Address"
          id="street_address"
          defaultValue={hotel.street_address}
          onChange={handleChange}
          disabled={disapled}
          required
        />
        <TextField
          variant="outlined"
          label="City"
          id="city"
          defaultValue={hotel.city}
          onChange={handleChange}
          disabled={disapled}
          required
        />

        <TextField
          variant="outlined"
          label="State"
          disabled={disapled}
          id="state"
          defaultValue={hotel.state}
          onChange={handleChange}
          required
        />
        <TextField
          variant="outlined"
          label="Zipcode"
          disabled={disapled}
          id="zipcode"
          defaultValue={hotel.zipcode}
          onChange={handleChange}
          required
        />
        <TextField
          variant="outlined"
          label="Phone Number"
          disabled={disapled}
          id="phone_number"
          defaultValue={hotel.phone_number}
          onChange={handleChange}
          required
        />

        <TextField
          label="Weekend Differential"
          id="weekend_diff_percentage"
          type="number"
          defaultValue={hotel.weekend_diff_percentage * 100}
          disabled={disapled}
          onChange={handleChange}
          InputProps={{
            endAdornment: <InputAdornment position="start">%</InputAdornment>
          }}
        />

        <FormControl
          disabled={disapled}
          className="grid-span"
          component="fieldset"
          variant="standard"
        >
          <FormLabel component="legend">Amenities</FormLabel>
          <FormGroup row sx={{ justifyContent: "space-between" }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={hotel.Pool}
                  onChange={event =>
                    setHotel({ ...hotel, Pool: event.target.checked })
                  }
                  id="Pool"
                />
              }
              label="Pool"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={hotel.Gym}
                  onChange={event =>
                    setHotel({ ...hotel, Gym: event.target.checked })
                  }
                  id="Gym"
                />
              }
              label="Gym"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={hotel.Spa}
                  onChange={event =>
                    setHotel({ ...hotel, Spa: event.target.checked })
                  }
                  id="Spa"
                />
              }
              label="Spa"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={hotel.Bussiness_Office}
                  onChange={event =>
                    setHotel({
                      ...hotel,
                      Bussiness_Office: event.target.checked
                    })
                  }
                  id="Bussiness_Office"
                />
              }
              label="Bussiness Office"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={hotel.Wifi}
                  onChange={event =>
                    setHotel({
                      ...hotel,
                      Wifi: event.target.checked
                    })
                  }
                  id="Wifi"
                />
              }
              label="Wifi"
            />
          </FormGroup>
        </FormControl>
        {user.isAdmin && (
          <>
            <FormLabel className="grid-span" disabled={disapled}>
              Rooms Information
            </FormLabel>

            <TextField
              variant="outlined"
              label="Standard Room Count"
              disabled={disapled}
              type="number"
              id="standard_count"
              defaultValue={hotel.standard_count}
              onChange={handleChange}
              required
            />
            <TextField
              variant="outlined"
              label="Standard Room Price"
              disabled={disapled}
              type="number"
              id="standard_price"
              defaultValue={hotel.standard_price}
              onChange={handleChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">$</InputAdornment>
                )
              }}
              required
            />
            <TextField
              variant="outlined"
              label="Queen Room Count"
              disabled={disapled}
              type="number"
              id="queen_count"
              defaultValue={hotel.queen_count}
              onChange={handleChange}
            />
            <TextField
              variant="outlined"
              label="Queen Room Price"
              disabled={disapled}
              type="number"
              id="queen_price"
              defaultValue={hotel.queen_price}
              onChange={handleChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">$</InputAdornment>
                )
              }}
            />
            <TextField
              variant="outlined"
              label="King Room Count"
              disabled={disapled}
              type="number"
              id="king_count"
              defaultValue={hotel.king_count}
              onChange={handleChange}
            />
            <TextField
              variant="outlined"
              label="King Room Price"
              disabled={disapled}
              type="number"
              id="king_price"
              defaultValue={hotel.king_price}
              onChange={handleChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">$</InputAdornment>
                )
              }}
            />

            <LoadingButton
              variant="contained"
              type="submit"
              size="large"
              disabled={disapled}
              loading={buttonLoading}
              loadingPosition="end"
              sx={{ borderRadius: "20px", mt: 3 }}
              className="grid-span"
              endIcon={<HotelIcon />}
            >
              Save
            </LoadingButton>
          </>
        )}
      </div>
    </Container>
  );
};

export default HotelForm;

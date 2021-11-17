import queryString from "query-string";
import { useState, useEffect } from "react";
import CheckInOutDates from "./common/CheckInOutDates";
import * as hotelService from "../services/hotelService";
import { totalNights, totalWeekends, formatDate } from "./utils/formatDate";
import Alert from "@mui/material/Alert";
import Hotel from "./common/Hotel";
import Slider from "@mui/material/Slider";
import Loading from "./common/Loading";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Button from "@mui/material/Button";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import ApartmentIcon from "@mui/icons-material/Apartment";
import TodayIcon from "@mui/icons-material/Today";
import EventIcon from "@mui/icons-material/Event";
import SingleBedIcon from "@mui/icons-material/SingleBed";
import BedIcon from "@mui/icons-material/Bed";
import KingBedIcon from "@mui/icons-material/KingBed";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";
import Checkbox from "@mui/material/Checkbox";
import FormControl from "@mui/material/FormControl";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormGroup from "@mui/material/FormGroup";
import LoadingButton from "@mui/lab/LoadingButton";
import { saveReservation } from "../services/reservationService";

const minDistance = 10;
const HotelSearch = ({ location, history }) => {
  const params = queryString.parse(location.search);
  const [date, setDate] = useState([
    new Date(params["check-in"]),
    new Date(params["check-out"])
  ]);
  const [city, setCity] = useState(params.city);
  const [dateError, setDateError] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [hotels, setHotels] = useState([]);
  const [price, setPrice] = useState([0, 500]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [reservation, setReservation] = useState(null);
  const [loadingBtn, setLoadingBtn] = useState(false);
  const [filter, setFilter] = useState({
    Pool: false,
    Gym: false,
    Spa: false,
    Business_Office: false,
    Wifi: false
  });
  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("sm"));

  const getHotels = async () => {
    setError("");
    try {
      const { data: hotels } = await hotelService.getHotelAvailability(
        formatDate(date[0]),
        formatDate(date[1]),
        city.trim()
      );
      setHotels(hotels);
    } catch (ex) {
      if (ex.response) {
        if (ex.response.status === 404) {
          setError(ex.response.data.message);
        } else {
          setError(JSON.stringify(ex.response.data));
        }
        setHotels([]);
      }
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    getHotels();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSearch = async event => {
    event.preventDefault();
    if (dateError) return;

    const nights = totalNights(date[1], date[0]);
    const weekends = totalWeekends(date[0], date[1]);

    setLoading(true);
    history.replace(
      `hotel-search?city=${city}&check-in=${date[0]}&check-out=${date[1]}&nights=${nights}&weekends=${weekends}`
    );
    getHotels();
  };

  const handlePriceChange = (event, newValue, activeThumb) => {
    if (!Array.isArray(newValue)) {
      return;
    }

    if (newValue[1] - newValue[0] < minDistance) {
      if (activeThumb === 0) {
        const clamped = Math.min(newValue[0], 1000 - minDistance);
        setPrice([clamped, clamped + minDistance]);
      } else {
        const clamped = Math.max(newValue[1], minDistance);
        setPrice([clamped - minDistance, clamped]);
      }
    } else {
      setPrice(newValue);
    }
  };

  const handleClickOpen = reservation => {
    if (!reservation.user_id) {
      history.push({
        pathname: "/signin",
        state: { from: location }
      });
      return;
    }
    setReservation(reservation);
    setOpen(true);
  };

  const handleConfirmReservation = async () => {
    try {
      setLoadingBtn(true);
      await saveReservation(reservation);
      const revisedHotels = hotels.map(hotel => {
        if (hotel.hotel_id === reservation.hotel_id) {
          hotel.available_standard_count =
            hotel.available_standard_count -
            reservation.reserved_standard_count;
          hotel.available_queen_count =
            hotel.available_queen_count - reservation.reserved_queen_count;
          hotel.available_king_count =
            hotel.available_king_count - reservation.reserved_king_count;
        }
        return hotel;
      });
      setHotels(revisedHotels);
      setSuccess(true);
    } catch (ex) {
      if (ex.response) {
        setError(JSON.stringify(ex.response.data));
      }
    } finally {
      setLoadingBtn(false);
    }
  };

  const handleClose = () => {
    setError("");
    setSuccess(false);
    setOpen(false);
  };

  const handleFilterChange = event => {
    setFilter({ ...filter, [event.target.id]: event.target.checked });
  };

  let filtered = hotels.filter(hotel => {
    if (
      hotel.available_king_count &&
      hotel.king_price <= price[1] &&
      (hotel.standard_price >= price[0] ||
        hotel.queen_price >= price[0] ||
        hotel.king_price >= price[0])
    ) {
      return true;
    } else if (
      hotel.available_queen_count &&
      hotel.queen_price <= price[1] &&
      (hotel.standard_price >= price[0] || hotel.queen_price >= price[0])
    ) {
      return true;
    } else if (
      hotel.standard_price <= price[1] &&
      hotel.standard_price >= price[0]
    ) {
      return true;
    } else {
      return false;
    }
  });

  if (filter.Pool) {
    filtered = filtered.filter(hotel => hotel.Pool);
  }
  if (filter.Gym) {
    filtered = filtered.filter(hotel => hotel.Gym);
  }
  if (filter.Spa) {
    filtered = filtered.filter(hotel => hotel.Spa);
  }
  if (filter.Business_Office) {
    filtered = filtered.filter(hotel => hotel.Business_Office);
  }
  if (filter.Wifi) {
    filtered = filtered.filter(hotel => hotel.Wifi);
  }

  return (
    <div className="hotel-search-block">
      <CheckInOutDates
        date={date}
        setDate={setDate}
        city={city}
        setCity={setCity}
        error={dateError}
        setError={setDateError}
        handleSearch={handleSearch}
        formContainerStyle="hotel-search-form-container"
        formStyle="hotel-search-form"
        btnStyle="hotel-search-btn"
      />
      {loading ? (
        <Loading />
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : (
        <div className="hotel-search-container">
          <div className="filter-container">
            <div>
              <span style={{ marginBottom: "5px" }}>Price Range</span>
              <Slider
                getAriaLabel={() => "Price Range"}
                value={price}
                onChange={handlePriceChange}
                getAriaValueText={value => `$${value}`}
                valueLabelDisplay="on"
                disableSwap
                color="secondary"
                max={500}
                sx={{ marginTop: "2.3rem" }}
              />
            </div>
            <div>
              <FormControl component="fieldset" variant="standard">
                <span style={{ margin: "10px 0" }}>Amenities</span>
                <FormGroup className="am">
                  <FormControlLabel
                    control={
                      <Checkbox
                        color="info"
                        id="Pool"
                        checked={filter.Pool}
                        onChange={handleFilterChange}
                      />
                    }
                    className="amenities"
                    label="Pool"
                  />

                  <FormControlLabel
                    control={
                      <Checkbox
                        color="info"
                        id="Gym"
                        checked={filter.Gym}
                        onChange={handleFilterChange}
                      />
                    }
                    label="Gym"
                    className="amenities"
                  />

                  <FormControlLabel
                    control={
                      <Checkbox
                        color="info"
                        id="Spa"
                        checked={filter.Spa}
                        onChange={handleFilterChange}
                      />
                    }
                    label="Spa"
                    className="amenities"
                  />

                  <FormControlLabel
                    control={
                      <Checkbox
                        color="info"
                        id="Business_Office"
                        checked={filter.Business_Office}
                        onChange={handleFilterChange}
                      />
                    }
                    label="Business_Office"
                    className="amenities"
                  />

                  <FormControlLabel
                    control={
                      <Checkbox
                        color="info"
                        id="Wifi"
                        checked={filter.Wifi}
                        onChange={handleFilterChange}
                      />
                    }
                    label="Wifi"
                    className="amenities"
                  />
                </FormGroup>
              </FormControl>
            </div>
          </div>

          {filtered.length === 0 ? (
            <h3 style={{ color: "red" }}>
              No Hotels to Show for the Specified Filters!
            </h3>
          ) : (
            <div className="hotel-search-hotels">
              {filtered.map(hotel => {
                return (
                  <Hotel
                    key={hotel.hotel_id}
                    hotel={hotel}
                    price={price}
                    location={location}
                    handleClickOpen={handleClickOpen}
                  />
                );
              })}
            </div>
          )}
        </div>
      )}
      {reservation && (
        <Dialog
          fullWidth
          fullScreen={fullScreen}
          open={open}
          onClose={handleClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">
            {error ? (
              <Alert severity="error">{error}</Alert>
            ) : success ? (
              <Alert severity="success">Reservation Confirmed</Alert>
            ) : (
              "Please Confirm Your Reservation!"
            )}
          </DialogTitle>
          <DialogContent>
            <div className="confirmation-container">
              <span className="grid-span">
                <div className="confirmation-icon-text">
                  <ApartmentIcon color="info" />
                  <span>
                    Hotel: <b>{reservation.hotel.hotel_name}</b>
                  </span>
                </div>
              </span>
              <span className="grid-span">
                <div className="confirmation-icon-text">
                  <LocationOnIcon color="info" />
                  <span>
                    Address:
                    <b>
                      {` ${reservation.hotel.street_address}, ${reservation.hotel.city},
                  ${reservation.hotel.state}, ${reservation.hotel.zipcode}`}
                    </b>
                  </span>
                </div>
              </span>
              <span>
                <div className="confirmation-icon-text">
                  <TodayIcon color="info" />
                  <span>
                    Check-in:
                    <b>
                      {` ${new Date(reservation.check_in).toLocaleDateString(
                        "en-US"
                      )}`}
                    </b>
                  </span>
                </div>
              </span>

              <span>
                <div className="confirmation-icon-text">
                  <EventIcon color="info" />
                  <span>
                    Check-out:
                    <b>
                      {` ${new Date(reservation.check_out).toLocaleDateString(
                        "en-US"
                      )}`}
                    </b>
                  </span>
                </div>
              </span>
              <div className="grid-span confirmation-reserved-rooms">
                {reservation.reserved_standard_count > 0 && (
                  <span>
                    <div className="confirmation-icon-text">
                      <b>{reservation.reserved_standard_count}X</b>
                      <SingleBedIcon color="info" />
                      <span>Standard Room</span>
                    </div>
                  </span>
                )}
                {reservation.reserved_queen_count > 0 && (
                  <span>
                    <div className="confirmation-icon-text">
                      <b>{reservation.reserved_queen_count}X</b>
                      <BedIcon color="info" />
                      <span>Queen Room</span>
                    </div>
                  </span>
                )}
                {reservation.reserved_king_count > 0 && (
                  <span>
                    <div className="confirmation-icon-text">
                      <b>{reservation.reserved_king_count}X</b>
                      <KingBedIcon color="info" />
                      <span>King Room</span>
                    </div>
                  </span>
                )}
              </div>
              <span className="reservation_total grid-span">
                <b>Total Price: ${reservation.total_price}</b>
              </span>
            </div>
          </DialogContent>
          <DialogActions>
            {success ? (
              <Button onClick={() => history.push("/my-reservations")}>
                Go To My Reservations
              </Button>
            ) : (
              <>
                <LoadingButton
                  variant="contained"
                  onClick={handleConfirmReservation}
                  loading={loadingBtn}
                >
                  Confirm
                </LoadingButton>
                <Button color="error" onClick={handleClose}>
                  Cancle
                </Button>
              </>
            )}
          </DialogActions>
        </Dialog>
      )}
    </div>
  );
};

export default HotelSearch;

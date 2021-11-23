import TextField from "@mui/material/TextField";
import LocalizationProvider from "@mui/lab/LocalizationProvider";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import isSameDay from "date-fns/isSameDay";
import { useState } from "react";
import LoadingButton from "@mui/lab/LoadingButton";
import MobileDateRangePicker from "@mui/lab/MobileDateRangePicker";
import { useEffect } from "react";
import * as reservationService from "../../services/reservationService";
import Loading from "./Loading";
import Alert from "@mui/material/Alert";

import {
  formatDate,
  formatDateToRegular,
  totalNights,
  totalPrice,
  totalWeekends
} from "../utils/formatDate";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import ApartmentIcon from "@mui/icons-material/Apartment";
import SingleBedIcon from "@mui/icons-material/SingleBed";
import BedIcon from "@mui/icons-material/Bed";
import KingBedIcon from "@mui/icons-material/KingBed";
import { Link } from "react-router-dom";
import { startOfToday, startOfTomorrow } from "date-fns";
import { getCurrentUser } from "../../services/authService";

const ReservationFrom = ({ match, history }) => {
  const [reservation, setReservation] = useState({});
  const [date, setDate] = useState([startOfToday(), startOfTomorrow()]);
  const [error, setError] = useState(false);
  const [pageError, setPageError] = useState("");
  const [loading, setLoading] = useState(true);
  const [nights, setNights] = useState(0);
  const [weekends, setWeekends] = useState(0);
  const [total, setTotal] = useState(0.0);
  const [success, setSuccess] = useState(false);
  const [buttonLoading, setButtonLoading] = useState(false);

  useEffect(() => {
    const getReservation = async () => {
      const reservationId = match.params.id;
      try {
        const { data: reservationInfo } =
          await reservationService.getReservation(reservationId);

        const check_in = new Date(
          formatDateToRegular(reservationInfo.check_in)
        );
        const check_out = new Date(
          formatDateToRegular(reservationInfo.check_out)
        );
        setReservation(reservationInfo);
        setDate([check_in, check_out]);
        setNights(totalNights(check_out, check_in));
        setWeekends(totalWeekends(check_in, check_out));
        setTotal(reservationInfo.total_price);
      } catch (ex) {
        if (ex.response) {
          if (ex.response.status === 404) {
            history.replace("/not-found");
          } else {
            setPageError(JSON.stringify(ex.response.data));
          }
        }
      } finally {
        setLoading(false);
      }
    };

    getReservation();
  }, [history, match]);

  const handleChange = event => {
    const newResevation = {
      ...reservation,
      [event.target.name]: parseInt(event.target.value)
    };
    const total = totalPrice(
      reservation.hotel_information.standard_price,
      reservation.hotel_information.queen_price,
      reservation.hotel_information.king_price,
      nights,
      weekends,
      reservation.hotel_information.weekend_diff_percentage,
      newResevation.reserved_standard_count,
      newResevation.reserved_queen_count,
      newResevation.reserved_king_count
    );

    setTotal(total);
    setReservation(newResevation);
  };
  const handleSubmit = async event => {
    event.preventDefault();
    setSuccess(false);
    setPageError(false);
    if (error) return;

    const updatedReservation = {
      ...reservation,
      check_in: formatDate(date[0]),
      check_out: formatDate(date[1]),
      total_price: total
    };

    try {
      setButtonLoading(true);
      await reservationService.updateReservation(
        updatedReservation.reservation_id,
        updatedReservation
      );
      setSuccess(true);
    } catch (ex) {
      if (ex.response) {
        if (ex.response.status === 400) {
          setPageError(JSON.stringify(ex.response.data.message));
        } else {
          setPageError(JSON.stringify(ex.response.data));
        }
      }
    } finally {
      setButtonLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (pageError) {
    return <h1>{pageError}</h1>;
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
      <div className="reservation-form-container">
        <h1 className="title">Reservation Information</h1>
        <div>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <MobileDateRangePicker
              disablePast={getCurrentUser()?.isAdmin ? false : true}
              startText="Check-in"
              endText="Check-out"
              value={date}
              onChange={newValue => {
                if (isSameDay(newValue[0], newValue[1])) {
                  setError(true);
                } else {
                  setError(false);
                }
                setDate(newValue);

                if (newValue[0] && newValue[1] && newValue[0] < newValue[1]) {
                  setNights(totalNights(newValue[1], newValue[0]));
                  setWeekends(totalWeekends(newValue[0], newValue[1]));
                  setTotal(
                    totalPrice(
                      reservation.hotel_information.standard_price,
                      reservation.hotel_information.queen_price,
                      reservation.hotel_information.king_price,
                      nights,
                      weekends,
                      reservation.hotel_information.weekend_diff_percentage,
                      reservation.reserved_standard_count,
                      reservation.reserved_queen_count,
                      reservation.reserved_king_count
                    )
                  );
                }
              }}
              renderInput={(startProps, endProps) => {
                return (
                  <Box className="reservation-form-grid">
                    {pageError && (
                      <Alert className="grid-span" severity="error">
                        {pageError}
                      </Alert>
                    )}
                    {success && (
                      <Alert
                        className="grid-span"
                        sx={{ textAlign: "center" }}
                        severity="success"
                      >
                        Reservation Info Saved!
                      </Alert>
                    )}
                    <div className="confirmation-icon-text grid-span">
                      <ApartmentIcon color="info" />
                      <span>
                        Hotel:{" "}
                        <b>
                          <Link
                            to={`/hotels/${reservation.hotel_information.hotel_id}`}
                          >
                            {reservation.hotel_information.hotel_name}
                          </Link>
                        </b>
                      </span>
                    </div>

                    <div className="confirmation-icon-text grid-span">
                      <LocationOnIcon color="info" />
                      <span>
                        Address:
                        <b>
                          {` ${reservation.hotel_information.street_address}, ${reservation.hotel_information.city},
                    ${reservation.hotel_information.state}, ${reservation.hotel_information.zipcode}`}
                        </b>
                      </span>
                    </div>

                    <TextField
                      margin="dense"
                      {...startProps}
                      error={error}
                      required
                    />
                    <TextField
                      margin="dense"
                      {...endProps}
                      error={error}
                      helperText={error ? "You can't choose same dates" : ""}
                      required
                    />
                    <div className="grid-span reservation-form-rooms-flex">
                      <div className="confirmation-icon-text">
                        <input
                          type="number"
                          name="reserved_standard_count"
                          defaultValue={reservation.reserved_standard_count}
                          className="reservation-from-container-input"
                          onChange={handleChange}
                          min="0"
                          max="5"
                        />
                        <SingleBedIcon color="info" />
                        <span>
                          <b>Standard Room</b>
                        </span>
                      </div>

                      <div className="confirmation-icon-text">
                        <input
                          type="number"
                          name="reserved_queen_count"
                          defaultValue={reservation.reserved_queen_count}
                          className="reservation-from-container-input"
                          onChange={handleChange}
                          min="0"
                          max="5"
                        />
                        <BedIcon color="info" />
                        <span>
                          <b>Queen Room</b>
                        </span>
                      </div>

                      <div className="confirmation-icon-text">
                        <input
                          type="number"
                          name="reserved_king_count"
                          defaultValue={reservation.reserved_king_count}
                          className="reservation-from-container-input"
                          onChange={handleChange}
                          min="0"
                          max="5"
                        />
                        <KingBedIcon color="info" />
                        <span>
                          <b>King Room</b>
                        </span>
                      </div>
                    </div>

                    <div
                      className="reservation_total grid-span"
                      style={{ fontSize: "1.4rem", marginTop: "2rem" }}
                    >
                      <span>
                        {getCurrentUser()?.isAdmin ? (
                          <div className="admin_total">
                            <b>Total Price: $</b>
                            <input
                              type="number"
                              value={total}
                              style={{ width: "auto" }}
                              className="reservation-from-container-input"
                              onChange={event => setTotal(event.target.value)}
                            />
                            <span style={{ fontSize: "1.3rem" }}>
                              for {nights + (nights > 1 ? " nights" : " night")}
                            </span>
                          </div>
                        ) : (
                          <>
                            <b>{`Total Price: $${total} `}</b>
                            <span style={{ fontSize: "1.3rem" }}>
                              for {nights + (nights > 1 ? " nights" : " night")}
                            </span>
                          </>
                        )}
                      </span>
                    </div>
                    <LoadingButton
                      variant="contained"
                      type="submit"
                      size="large"
                      sx={{ borderRadius: "20px", mt: 5 }}
                      className="grid-span"
                      loading={buttonLoading}
                    >
                      Update
                    </LoadingButton>
                  </Box>
                );
              }}
            />
          </LocalizationProvider>
        </div>
      </div>
    </Container>
  );
};

export default ReservationFrom;

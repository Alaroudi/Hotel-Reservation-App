import { useEffect, useState } from "react";
import auth from "../services/authService";
import {
  DeleteReservation,
  getUserReservations
} from "../services/reservationService";
import Loading from "./common/Loading";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import ApartmentIcon from "@mui/icons-material/Apartment";
import TodayIcon from "@mui/icons-material/Today";
import EventIcon from "@mui/icons-material/Event";
import SingleBedIcon from "@mui/icons-material/SingleBed";
import BedIcon from "@mui/icons-material/Bed";
import KingBedIcon from "@mui/icons-material/KingBed";
import { Link } from "react-router-dom";
import { formatDateToRegular } from "./utils/formatDate";

const MyReservations = ({ history }) => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState();

  useEffect(() => {
    const getMyReservations = async () => {
      try {
        setLoading(true);
        const user_id = auth.getCurrentUser()?.id;
        const reservations = await getUserReservations(user_id);
        setReservations(reservations.data);
      } catch (ex) {
        if (ex.response && ex.response.status === 404) {
          setError("You Do not Have Any Reservations  Yet!");
        }
      } finally {
        setLoading(false);
      }
    };

    getMyReservations();
  }, []);

  const handleDeleteReservation = async reservation_id => {
    try {
      await DeleteReservation(reservation_id);
      setReservations(
        reservations.filter(
          reservation => reservation.reservation_id !== reservation_id
        )
      );
    } catch (ex) {
      if (ex.response && ex.response.status === 404) {
        setError(ex.response.data.message);
        console.log(ex.response.data.message);
      }
    }
  };

  if (loading) return <Loading />;

  const renderErrorMessage = message => {
    return (
      <div
        style={{
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          height: "100%"
        }}
      >
        <h1 style={{ fontWeight: "400" }}>{error || message}</h1>
        <Button onClick={() => history.push("/")}>Make a reservation</Button>
      </div>
    );
  };
  if (error) {
    renderErrorMessage();
  }
  const PastReservations = reservations.filter(reservation => {
    const todayDate = new Date().setHours(0, 0, 0, 0);
    const checkInDate = new Date(formatDateToRegular(reservation.check_in));

    if (checkInDate < todayDate) {
      return true;
    }
    return false;
  });
  const FutureReservations = reservations.filter(reservation => {
    const todayDate = new Date().setHours(0, 0, 0, 0);
    const checkInDate = new Date(formatDateToRegular(reservation.check_in));

    if (checkInDate >= todayDate) {
      return true;
    }
    return false;
  });

  return (
    <div className="myreservation-container">
      {reservations.length === 0 ? (
        renderErrorMessage("There is No Reservations to Show!")
      ) : (
        <div className="hotel-search-hotels">
          {FutureReservations.length > 0 && (
            <>
              <h3
                style={{
                  fontWeight: "400",
                  marginLeft: "0.5rem"
                }}
              >
                Future Reservations
              </h3>
              {FutureReservations.map(reservation => (
                <div key={reservation.reservation_id} className="hotel flex">
                  <div className="modify-btns">
                    <Button
                      variant="outlined"
                      color="info"
                      endIcon={<EditIcon />}
                      onClick={() =>
                        history.push(
                          `/reservations/${reservation.reservation_id}`
                        )
                      }
                    >
                      Edit
                    </Button>
                    <Button
                      variant="outlined"
                      color="error"
                      endIcon={<DeleteIcon />}
                      onClick={() =>
                        handleDeleteReservation(reservation.reservation_id)
                      }
                    >
                      Delete
                    </Button>
                  </div>
                  <div className="reservation-container">
                    <span>
                      <div className="confirmation-icon-text">
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
                    </span>
                    <span>
                      <div className="confirmation-icon-text">
                        <LocationOnIcon color="info" />
                        <span>
                          Address:
                          <b>
                            {` ${reservation.hotel_information.street_address}, ${reservation.hotel_information.city},
                      ${reservation.hotel_information.state}, ${reservation.hotel_information.zipcode}`}
                          </b>
                        </span>
                      </div>
                    </span>
                    <span>
                      <div className="confirmation-icon-text">
                        <TodayIcon color="info" />
                        <span>
                          Check-in:
                          <b>{` ${formatDateToRegular(
                            reservation.check_in
                          )}`}</b>
                        </span>
                      </div>
                    </span>
                    <span>
                      <div className="confirmation-icon-text">
                        <EventIcon color="info" />
                        <span>
                          Check-out:
                          <b>{` ${formatDateToRegular(
                            reservation.check_out
                          )}`}</b>
                        </span>
                      </div>
                    </span>
                    <span>Reserved Rooms:</span>
                    {reservation.reserved_standard_count > 0 && (
                      <span>
                        <div className="confirmation-icon-text">
                          <b>{reservation.reserved_standard_count}X</b>
                          <SingleBedIcon color="info" />
                          <span>
                            <b>Standard Room</b>
                          </span>
                        </div>
                      </span>
                    )}
                    {reservation.reserved_queen_count > 0 && (
                      <span>
                        <div className="confirmation-icon-text">
                          <b>{reservation.reserved_queen_count}X</b>
                          <BedIcon color="info" />
                          <span>
                            <b>Queen Room</b>
                          </span>
                        </div>
                      </span>
                    )}
                    {reservation.reserved_king_count > 0 && (
                      <span>
                        <div className="confirmation-icon-text">
                          <b>{reservation.reserved_king_count}X</b>
                          <KingBedIcon color="info" />
                          <span>
                            <b>King Room</b>
                          </span>
                        </div>
                      </span>
                    )}
                    <span className="reservation_total grid-span">
                      <b>Total Price: ${reservation.total_price}</b>
                    </span>
                  </div>
                </div>
              ))}
            </>
          )}
          {PastReservations.length > 0 && (
            <>
              <h3 style={{ fontWeight: "400", marginLeft: "0.5rem" }}>
                Past Reservations
              </h3>
              {PastReservations.map(reservation => (
                <div key={reservation.reservation_id} className="hotel flex">
                  <div className="reservation-container">
                    <span>
                      <div className="confirmation-icon-text">
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
                    </span>
                    <span>
                      <div className="confirmation-icon-text">
                        <LocationOnIcon color="info" />
                        <span>
                          Address:
                          <b>
                            {` ${reservation.hotel_information.street_address}, ${reservation.hotel_information.city},
                      ${reservation.hotel_information.state}, ${reservation.hotel_information.zipcode}`}
                          </b>
                        </span>
                      </div>
                    </span>
                    <span>
                      <div className="confirmation-icon-text">
                        <TodayIcon color="info" />
                        <span>
                          Check-in:
                          <b>{` ${formatDateToRegular(
                            reservation.check_in
                          )}`}</b>
                        </span>
                      </div>
                    </span>
                    <span>
                      <div className="confirmation-icon-text">
                        <EventIcon color="info" />
                        <span>
                          Check-out:
                          <b>{` ${formatDateToRegular(
                            reservation.check_out
                          )}`}</b>
                        </span>
                      </div>
                    </span>
                    <span>Reserved Rooms:</span>
                    {reservation.reserved_standard_count > 0 && (
                      <span>
                        <div className="confirmation-icon-text">
                          <b>{reservation.reserved_standard_count}X</b>
                          <SingleBedIcon color="info" />
                          <span>
                            <b>Standard Room</b>
                          </span>
                        </div>
                      </span>
                    )}
                    {reservation.reserved_queen_count > 0 && (
                      <span>
                        <div className="confirmation-icon-text">
                          <b>{reservation.reserved_queen_count}X</b>
                          <BedIcon color="info" />
                          <span>
                            <b>Queen Room</b>
                          </span>
                        </div>
                      </span>
                    )}
                    {reservation.reserved_king_count > 0 && (
                      <span>
                        <div className="confirmation-icon-text">
                          <b>{reservation.reserved_king_count}X</b>
                          <KingBedIcon color="info" />
                          <span>
                            <b>King Room</b>
                          </span>
                        </div>
                      </span>
                    )}
                    <span className="reservation_total grid-span">
                      <b>Total Price: ${reservation.total_price}</b>
                    </span>
                  </div>
                </div>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default MyReservations;

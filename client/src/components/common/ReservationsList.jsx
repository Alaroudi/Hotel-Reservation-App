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
import { DeleteReservation } from "../../services/reservationService";
import { useState } from "react";

const ReservationsList = ({
  userReservations,
  history,
  setError,
  users,
  setUsers,
  userId
}) => {
  const [reservations, setReservations] = useState(userReservations);

  const handleDeleteReservation = async reservation_id => {
    try {
      await DeleteReservation(reservation_id);
      const modifiedReservations = reservations.filter(
        reservation => reservation.reservation_id !== reservation_id
      );
      setReservations(modifiedReservations);

      setUsers(
        users.map(user => {
          if (user.user_id === userId) {
            user.reservations = modifiedReservations;
          }
          return user;
        })
      );
    } catch (ex) {
      if (ex.response && ex.response.status === 404) {
        setError(ex.response.data.message);
      }
    }
  };
  return (
    <div className="hotel-search-hotels no-padding">
      {reservations.map(reservation => (
        <div key={reservation.reservation_id} className="hotel flex">
          <div className="modify-btns">
            <Button
              variant="outlined"
              color="info"
              endIcon={<EditIcon />}
              onClick={() =>
                history.push(`reservations/${reservation.reservation_id}`)
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
                      to={`hotels/${reservation.hotel_information.hotel_id}`}
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
                    <b>King Room</b>s
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
    </div>
  );
};

export default ReservationsList;

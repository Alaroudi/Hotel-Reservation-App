import Button from "@mui/material/Button";
import Checkbox from "@mui/material/Checkbox";
import FormControl from "@mui/material/FormControl";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormGroup from "@mui/material/FormGroup";
import FormLabel from "@mui/material/FormLabel";
import queryString from "query-string";
import { useState } from "react";
import { formatDate, totalPrice } from "../utils/formatDate";
import auth from "../../services/authService";
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";

const Hotel = ({ hotel, price, location, handleClickOpen }) => {
  const params = queryString.parse(location.search);
  const nights = parseInt(params.nights);
  const weekends = parseInt(params.weekends);
  const [reservation, setReservation] = useState({
    user_id: auth.getCurrentUser()?.id,
    hotel_id: hotel.hotel_id,
    hotel: hotel,
    check_in: formatDate(new Date(params["check-in"])),
    check_out: formatDate(new Date(params["check-out"])),
    total_price: 0.0,
    reserved_standard_count: 0,
    reserved_queen_count: 0,
    reserved_king_count: 0
  });

  const handleSelection = event => {
    const newResevation = {
      ...reservation,
      [event.target.id]: parseInt(event.target.value)
    };
    const total = totalPrice(
      hotel.standard_price,
      hotel.queen_price,
      hotel.king_price,
      nights,
      weekends,
      hotel.weekend_diff_percentage,
      newResevation.reserved_standard_count,
      newResevation.reserved_queen_count,
      newResevation.reserved_king_count
    );

    setReservation({
      ...newResevation,
      total_price: total
    });
  };

  return (
    <div className="hotel">
      <h2>{hotel.hotel_name}</h2>
      <p>
        {`${hotel.street_address}, ${hotel.city}, ${hotel.state}, ${hotel.zipcode}`}
        <br />
        {hotel.phone_number}
      </p>

      <FormControl component="fieldset" variant="standard">
        <FormLabel component="legend" focused>
          Amenities
        </FormLabel>
        <FormGroup row>
          {hotel.Pool && (
            <FormControlLabel
              sx={{ cursor: "default" }}
              control={
                <Checkbox
                  checked
                  disableRipple
                  sx={{ cursor: "default" }}
                  color="info"
                />
              }
              label="Pool"
            />
          )}
          {hotel.Gym && (
            <FormControlLabel
              sx={{ cursor: "default" }}
              control={
                <Checkbox
                  checked
                  disableRipple
                  sx={{ cursor: "default" }}
                  color="info"
                />
              }
              label="Gym"
            />
          )}
          {hotel.Spa && (
            <FormControlLabel
              sx={{ cursor: "default" }}
              control={
                <Checkbox
                  checked
                  disableRipple
                  sx={{ cursor: "default" }}
                  color="info"
                />
              }
              label="Spa"
            />
          )}
          {hotel.Business_Office && (
            <FormControlLabel
              sx={{ cursor: "default" }}
              control={
                <Checkbox
                  checked
                  disableRipple
                  sx={{ cursor: "default" }}
                  color="info"
                />
              }
              label="Business Office"
            />
          )}
          {hotel.Wifi && (
            <FormControlLabel
              sx={{ cursor: "default" }}
              control={
                <Checkbox
                  checked
                  disableRipple
                  sx={{ cursor: "default" }}
                  color="info"
                />
              }
              label="Wifi"
            />
          )}
        </FormGroup>
      </FormControl>
      <FormLabel component="legend" focused sx={{ marginTop: "0.5rem" }}>
        Rooms Available
      </FormLabel>
      {Boolean(weekends) && (
        <>
          <span className="card__diff">{`includes ${
            hotel.weekend_diff_percentage * 100
          }% weekend differential`}</span>
        </>
      )}
      <div className="card-container">
        {hotel.available_standard_count > 0 &&
        hotel.standard_price >= price[0] &&
        hotel.standard_price <= price[1] ? (
          <div className="card_flex">
            <div className="card">
              <h3>Standard Room</h3>
              <span className="card__price">${hotel.standard_price}</span>
              <span className="card__billing">/night</span>

              <div className="card__total">
                <div className="selection-container">
                  <label htmlFor="reserved_standard_count">
                    Select number of rooms:
                  </label>
                  <select
                    name="reserved_standard_count"
                    id="reserved_standard_count"
                    onChange={handleSelection}
                  >
                    <option value="0">select</option>
                    {[
                      ...new Array(Math.min(hotel.available_standard_count, 10))
                    ].map((element, index) => (
                      <option key={index} value={index + 1}>
                        {index + 1}
                      </option>
                    ))}
                  </select>
                </div>
                {hotel.available_standard_count <= 5 && (
                  <div className="confirmation-icon-text alert">
                    <ErrorOutlineIcon />
                    <span>Only {hotel.available_standard_count} left!</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : null}
        {hotel.available_queen_count > 0 &&
        hotel.queen_price >= price[0] &&
        hotel.queen_price <= price[1] ? (
          <div className="card_flex">
            <div className="card">
              <h3>Queen Room</h3>
              <div>
                <span className="card__price">${hotel.queen_price}</span>
                <span className="card__billing">/night</span>
              </div>
              <div className="card__total">
                <div className="selection-container">
                  <label htmlFor="reserved_queen_count">
                    Select number of rooms:
                  </label>
                  <select
                    name="reserved_queen_count"
                    id="reserved_queen_count"
                    onChange={handleSelection}
                  >
                    <option value="0">select</option>
                    {[
                      ...new Array(Math.min(hotel.available_queen_count, 10))
                    ].map((element, index) => (
                      <option key={index} value={index + 1}>
                        {index + 1}
                      </option>
                    ))}
                  </select>
                </div>
                {hotel.available_queen_count <= 5 && (
                  <div className="confirmation-icon-text alert">
                    <ErrorOutlineIcon />
                    <span>Only {hotel.available_queen_count} left!</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : null}
        {hotel.available_king_count > 0 &&
        hotel.king_price >= price[0] &&
        hotel.king_price <= price[1] ? (
          <div className="card_flex">
            <div className="card">
              <h3>King Room</h3>
              <span className="card__price">${hotel.king_price}</span>
              <span className="card__billing">/night</span>
              <div className="card__total">
                <div className="selection-container">
                  <label htmlFor="reserved_king_count">
                    Select number of rooms:
                  </label>
                  <select
                    name="reserved_king_count"
                    id="reserved_king_count"
                    onChange={handleSelection}
                  >
                    <option value="0">select</option>
                    {[
                      ...new Array(Math.min(hotel.available_king_count, 10))
                    ].map((element, index) => (
                      <option key={index} value={index + 1}>
                        {index + 1}
                      </option>
                    ))}
                  </select>
                </div>
                {hotel.available_king_count <= 5 && (
                  <div className="confirmation-icon-text alert">
                    <ErrorOutlineIcon />
                    <span>Only {hotel.available_king_count} left!</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : null}
      </div>
      {reservation.total_price > 0 && (
        <>
          <div className="total_price">
            <span>
              <b>{`Total Price: $${reservation.total_price}`}</b> for{" "}
              {nights + (nights > 1 ? " nights" : " night")}
            </span>
          </div>
          <div className="reserve-btn">
            <Button
              variant="outlined"
              color="secondary"
              value="standard"
              fullWidth
              onClick={() => handleClickOpen(reservation)}
            >
              Reserve
            </Button>
          </div>
        </>
      )}
    </div>
  );
};

export default Hotel;

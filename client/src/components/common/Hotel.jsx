import Checkbox from "@mui/material/Checkbox";
import FormControl from "@mui/material/FormControl";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormGroup from "@mui/material/FormGroup";
import FormLabel from "@mui/material/FormLabel";

const Hotel = ({ hotel, price }) => {
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
          {Boolean(hotel.Pool) && (
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
              className="amenities"
              label="Pool"
            />
          )}
          {Boolean(hotel.Gym) && (
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
              className="amenities"
            />
          )}
          {Boolean(hotel.Spa) && (
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
              className="amenities"
            />
          )}
          {Boolean(hotel.Business_Office) && (
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
              className="amenities"
            />
          )}
          {Boolean(hotel.Wifi) && (
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
              className="amenities"
            />
          )}
        </FormGroup>
      </FormControl>
      <FormLabel component="legend" focused sx={{ marginTop: "0.5rem" }}>
        Rooms Available
      </FormLabel>
      <div className="card-container">
        {hotel.available_standard_count &&
        hotel.standard_price >= price[0] &&
        hotel.standard_price <= price[1] ? (
          <div className="card">
            <h3>Standard Room</h3>
            <span className="card__price">${hotel.standard_price}</span>
            <span className="card__billing">/night</span>
          </div>
        ) : null}
        {hotel.available_queen_count &&
        hotel.queen_price >= price[0] &&
        hotel.queen_price <= price[1] ? (
          <div className="card">
            <h3>Queen Room</h3>
            <span className="card__price">${hotel.queen_price}</span>
            <span className="card__billing">/night</span>
          </div>
        ) : null}
        {hotel.available_king_count &&
        hotel.king_price >= price[0] &&
        hotel.king_price <= price[1] ? (
          <div className="card">
            <h3>King Room</h3>
            <span className="card__price">${hotel.king_price}</span>
            <span className="card__billing">/night</span>
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default Hotel;

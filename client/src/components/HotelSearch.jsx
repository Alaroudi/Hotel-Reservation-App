import queryString from "query-string";
import { useState, useEffect } from "react";
import CheckInOutDates from "./common/CheckInOutDates";
import * as hotelService from "../services/hotelService";
import formatDate from "./utils/formatDate";
import Alert from "@mui/material/Alert";
import Hotel from "./common/Hotel";
import Slider from "@mui/material/Slider";
import Loading from "./common/Loading";

// import {
//   // differenceInCalendarDays,
//   // eachWeekendOfInterval,
//   // subDays,
//   // format,
//   // isSameDay,
//   startOfToday,
//   startOfTomorrow
// } from "date-fns";
// function getStandardFormattedDateTime(date) {
//   return format(date, "yyyy-MM-dd");
// }
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
  const [hotels, setHotels] = useState([]);
  const [price, setPrice] = useState([0, 500]);
  const [loading, setLoading] = useState(true);

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
          setHotels([]);
        }
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

    setLoading(true);
    history.replace(
      `hotel-search?city=${city}&check-in=${date[0]}&check-out=${date[1]}`
    );
    getHotels();

    // const nights = differenceInCalendarDays(value[1], value[0]);
    // const weekends = eachWeekendOfInterval({
    //   start: value[0],
    //   end: subDays(value[1], 1)
    // }).length;
    // const search = {
    //   "check-in": getStandardFormattedDateTime(value[0]),
    //   "check-out": getStandardFormattedDateTime(value[1]),
    //   city: city,
    //   nights: nights - weekends,
    //   weekends: weekends
    // };
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

  const filtered = hotels.filter(hotel => {
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
            <span style={{ textAlign: "center", marginBottom: "5px" }}>
              Price Range
            </span>
            <Slider
              getAriaLabel={() => "Price Range"}
              value={price}
              onChange={handlePriceChange}
              getAriaValueText={value => `$${value}`}
              valueLabelDisplay="auto"
              disableSwap
              color="secondary"
              max={500}
              sx={{ marginTop: "2rem" }}
            />
          </div>
          {filtered.length === 0 ? (
            <h3 style={{ color: "red" }}>
              No Hotels to Show for the Specified Filters!
            </h3>
          ) : (
            <div className="hotel-search-hotels">
              {filtered.map(hotel => {
                return (
                  <Hotel key={hotel.hotel_id} hotel={hotel} price={price} />
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default HotelSearch;

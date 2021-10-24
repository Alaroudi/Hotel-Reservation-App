import LocalizationProvider from "@mui/lab/LocalizationProvider";
import TextField from "@mui/material/TextField";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import Box from "@mui/material/Box";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import { useState } from "react";
import {
  differenceInCalendarDays,
  eachWeekendOfInterval,
  subDays,
  format,
  isSameDay
} from "date-fns";
import { Button, InputAdornment } from "@mui/material";
import { MobileDateRangePicker } from "@mui/lab";

function getStandardFormattedDateTime(date) {
  return format(date, "yyyy-MM-dd");
}
const CheckInOutDates = () => {
  const [value, setValue] = useState([null, null]);
  const [error, setError] = useState(false);
  const [city, setCity] = useState("");

  const handleSubmit = event => {
    event.preventDefault();
    if (error) return;
    const nights = differenceInCalendarDays(value[1], value[0]);
    const weekends = eachWeekendOfInterval({
      start: value[0],
      end: subDays(value[1], 1)
    }).length;
    console.log({
      "check-in": getStandardFormattedDateTime(value[0]),
      "check-out": getStandardFormattedDateTime(value[1]),
      city: city,
      nights: nights - weekends,
      weekends: weekends
    });
  };
  return (
    <div className="check-in-out-container">
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <MobileDateRangePicker
          startText="Check-in"
          endText="Check-out"
          value={value}
          disablePast
          onChange={newValue => {
            if (isSameDay(newValue[0], newValue[1])) {
              setError(true);
            } else {
              setError(false);
            }
            setValue(newValue);
          }}
          renderInput={(startProps, endProps) => {
            return (
              <Box
                component="form"
                className="check-in-out-form"
                onSubmit={handleSubmit}
              >
                <TextField
                  sx={{ gridColumn: "1/-1" }}
                  placeholder="Going to"
                  required
                  value={city}
                  onChange={event => setCity(event.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <LocationOnIcon />
                      </InputAdornment>
                    )
                  }}
                />
                <TextField {...startProps} error={error} required />
                <TextField
                  {...endProps}
                  error={error}
                  helperText={error ? "You can't choose same dates" : ""}
                  required
                />
                <Button
                  variant="contained"
                  type="submit"
                  size="large"
                  sx={{
                    borderRadius: "20px",
                    gridColumn: "1/-1",
                    mt: "2rem",
                    width: "80%",
                    justifySelf: "center"
                  }}
                >
                  Search
                </Button>
              </Box>
            );
          }}
        />
      </LocalizationProvider>
    </div>
  );
};

export default CheckInOutDates;

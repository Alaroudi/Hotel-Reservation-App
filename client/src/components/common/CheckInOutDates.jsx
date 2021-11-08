import LocalizationProvider from "@mui/lab/LocalizationProvider";
import TextField from "@mui/material/TextField";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import Box from "@mui/material/Box";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import isSameDay from "date-fns/isSameDay";
import Button from "@mui/material/Button";
import InputAdornment from "@mui/material/InputAdornment";
import { MobileDateRangePicker } from "@mui/lab";

const CheckInOutDates = ({
  date,
  setDate,
  city,
  setCity,
  error,
  setError,
  handleSearch,
  formContainerStyle,
  formStyle,
  btnStyle,
  gridSpan
}) => {
  return (
    <div className={formContainerStyle}>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <MobileDateRangePicker
          startText="Check-in"
          endText="Check-out"
          value={date}
          disablePast
          onChange={newValue => {
            if (isSameDay(newValue[0], newValue[1])) {
              setError(true);
            } else {
              setError(false);
            }
            setDate(newValue);
          }}
          renderInput={(startProps, endProps) => {
            return (
              <Box
                component="form"
                className={formStyle}
                onSubmit={handleSearch}
              >
                <TextField
                  className={gridSpan ? "grid-span" : ""}
                  placeholder="Going to"
                  label="City"
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
                  className={btnStyle}
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

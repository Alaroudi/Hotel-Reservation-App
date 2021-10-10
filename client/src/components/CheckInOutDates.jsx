import LocalizationProvider from "@mui/lab/LocalizationProvider";
import TextField from "@mui/material/TextField";
import DateRangePicker from "@mui/lab/DateRangePicker";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import Box from "@mui/material/Box";
import { useState } from "react";
import {
  differenceInCalendarDays,
  eachWeekendOfInterval,
  subDays
} from "date-fns";

const CheckInOutDates = () => {
  const [value, setValue] = useState([null, null]);
  return (
    <div>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <DateRangePicker
          startText="Check-in"
          endText="Check-out"
          value={value}
          onChange={newValue => {
            setValue(newValue);
          }}
          renderInput={(startProps, endProps) => (
            <>
              <TextField {...startProps} />
              <Box sx={{ mx: 2 }}> to </Box>
              <TextField {...endProps} />
            </>
          )}
        />
      </LocalizationProvider>

      {value[0] &&
        value[1] &&
        console.log(
          "Total nights: " +
            differenceInCalendarDays(value[1], value[0]) +
            ", # of weekends: " +
            eachWeekendOfInterval({
              start: value[0],
              end: subDays(value[1], 1)
            }).length
        )}
    </div>
  );
};

export default CheckInOutDates;

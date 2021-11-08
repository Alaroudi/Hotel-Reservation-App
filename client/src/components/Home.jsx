import CheckInOutDates from "./common/CheckInOutDates";
import "./Home.css";
import { startOfToday, startOfTomorrow } from "date-fns";
import { useState } from "react";

function Home({ history }) {
  const [date, setDate] = useState([startOfToday(), startOfTomorrow()]);
  const [city, setCity] = useState("");
  const [error, setError] = useState(false);

  const handleSearch = event => {
    event.preventDefault();
    if (error) return;

    history.push(
      `hotel-search?city=${city}&check-in=${date[0]}&check-out=${date[1]}`
    );
  };
  return (
    <div className="home-container">
      <CheckInOutDates
        date={date}
        setDate={setDate}
        city={city}
        setCity={setCity}
        error={error}
        setError={setError}
        handleSearch={handleSearch}
        formContainerStyle="check-in-out-container"
        formStyle="check-in-out-form"
        gridSpan
        btnStyle="check-in-out-btn"
      />
    </div>
  );
}

export default Home;

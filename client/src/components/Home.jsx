import React from "react";
import CheckInOutDates from "./CheckInOutDates";
import "./Home.css";
function Home({ match }) {
  return (
    <div className="home-container">
      <CheckInOutDates />
    </div>
  );
}

export default Home;

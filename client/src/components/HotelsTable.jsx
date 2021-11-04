import React, { useEffect, useState } from "react";
import * as hotelService from "../services/hotelService";
import Loading from "./common/Loading";
import "./Hotels.css";
import { styled } from "@mui/material/styles";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";
import ApartmentIcon from "@mui/icons-material/Apartment";
const HotelsTable = ({ history }) => {
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    const getHotels = async () => {
      try {
        const hotels = await hotelService.getHotels();
        setHotels(hotels.data);
      } catch (ex) {
        if (ex.response && ex.response.status === 404) {
          setError(ex.response.data);
        }
      } finally {
        setLoading(false);
      }
    };
    getHotels();
  }, []);

  if (loading) return <Loading />;
  if (error) {
    return <h1>{error}</h1>;
  }

  const handleDelete = async hotel_id => {
    try {
      await hotelService.deleteHotel(hotel_id);
      setHotels(hotels.filter(hotel => hotel.hotel_id !== hotel_id));
    } catch (ex) {
      if (ex.response && ex.response.status === 404) {
        history.push("/not-found");
      }
    }
  };

  const handleTableCellClick = hotel_id => {
    history.push(`/hotels/${hotel_id}`);
  };

  const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
      backgroundColor: theme.palette.common.black,
      color: theme.palette.common.white
    },
    [`&.${tableCellClasses.body}`]: {
      fontSize: 14
    }
  }));

  const StyledTableRow = styled(TableRow)(({ theme }) => ({
    "&:nth-of-type(odd)": {
      backgroundColor: theme.palette.action.hover
    },
    // hide last border
    "&:last-child td, &:last-child th": {
      border: 0
    }
  }));

  return (
    <div className="hotel-container">
      <div
        style={{
          marginBottom: "1rem",
          marginTop: "0.5rem",
          textAlign: "right"
        }}
      >
        <Button
          variant="contained"
          color="secondary"
          size="large"
          onClick={() => history.push("/hotels/new")}
          startIcon={<ApartmentIcon />}
        >
          Create New Hotel
        </Button>
      </div>
      <p
        style={{ color: "#3e4246" }}
      >{`Showing ${hotels.length} hotels in the database.`}</p>
      <TableContainer component={Paper}>
        <Table aria-label="customized table">
          <TableHead>
            <TableRow>
              <StyledTableCell>Hotel Name</StyledTableCell>
              <StyledTableCell>Address</StyledTableCell>
              <StyledTableCell>Phone Number</StyledTableCell>
              <StyledTableCell>Amenities</StyledTableCell>
              <StyledTableCell>Rooms Information</StyledTableCell>
              <StyledTableCell>Weekend Differential</StyledTableCell>
              <StyledTableCell>Action</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {hotels.map(hotel => (
              <StyledTableRow key={hotel.hotel_id}>
                <StyledTableCell
                  onClick={() => handleTableCellClick(hotel.hotel_id)}
                  className="pointer"
                >
                  <b style={{ color: "#1976d2" }}>{hotel.hotel_name}</b>
                </StyledTableCell>

                <StyledTableCell
                  className="pointer"
                  onClick={() => handleTableCellClick(hotel.hotel_id)}
                >{`${hotel.street_address}, ${hotel.city}, ${hotel.state}, ${hotel.zipcode} `}</StyledTableCell>
                <StyledTableCell
                  className="pointer"
                  onClick={() => handleTableCellClick(hotel.hotel_id)}
                >
                  {hotel.phone_number}
                </StyledTableCell>
                <StyledTableCell
                  className="pointer"
                  onClick={() => handleTableCellClick(hotel.hotel_id)}
                >
                  <ul>
                    {hotel.amenities.length === 0
                      ? "None"
                      : hotel.amenities.map((amenity, index) => (
                          <li key={index}> {amenity} </li>
                        ))}
                  </ul>
                </StyledTableCell>
                <StyledTableCell
                  className="pointer"
                  onClick={() => handleTableCellClick(hotel.hotel_id)}
                >
                  <table className="inner-table">
                    <tbody>
                      <tr>
                        <td>
                          <b>Type</b>
                        </td>
                        <td>
                          <b>Count</b>
                        </td>
                        <td>
                          <b>Price</b>
                        </td>
                      </tr>

                      {hotel.standard_count ? (
                        <tr>
                          <td>Standard</td>
                          <td>{hotel.standard_count}</td>

                          <td>{"$" + hotel.standard_price}</td>
                        </tr>
                      ) : null}
                      {hotel.queen_count ? (
                        <tr>
                          <td>Queen</td>
                          <td>{hotel.queen_count}</td>

                          <td>{"$" + hotel.queen_price}</td>
                        </tr>
                      ) : null}
                      {hotel.king_count ? (
                        <tr>
                          <td>King</td>
                          <td>{hotel.king_count}</td>

                          <td>{"$" + hotel.king_price}</td>
                        </tr>
                      ) : null}
                    </tbody>
                  </table>
                </StyledTableCell>
                <StyledTableCell
                  className="pointer"
                  onClick={() => handleTableCellClick(hotel.hotel_id)}
                >
                  {`${hotel.weekend_diff_percentage * 100}%`}
                </StyledTableCell>
                <StyledTableCell>
                  <Button
                    variant="contained"
                    color="error"
                    endIcon={<DeleteIcon />}
                    onClick={() => handleDelete(hotel.hotel_id)}
                  >
                    Delete
                  </Button>
                </StyledTableCell>
              </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default HotelsTable;

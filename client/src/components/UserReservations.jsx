import { styled } from "@mui/material/styles";
import ArrowForwardIosSharpIcon from "@mui/icons-material/ArrowForwardIosSharp";
import MuiAccordion from "@mui/material/Accordion";
import MuiAccordionSummary from "@mui/material/AccordionSummary";
import MuiAccordionDetails from "@mui/material/AccordionDetails";
import { getReservations } from "../services/reservationService";
import { useState, useEffect } from "react";
import Loading from "./common/Loading";
import ReservationsList from "./common/ReservationsList";

const Accordion = styled(props => (
  <MuiAccordion disableGutters elevation={0} square {...props} />
))(({ theme }) => ({
  border: `1px solid ${theme.palette.divider}`,
  "&:not(:last-child)": {
    borderBottom: 0
  },
  "&:before": {
    display: "none"
  }
}));

const AccordionSummary = styled(props => (
  <MuiAccordionSummary
    expandIcon={<ArrowForwardIosSharpIcon sx={{ fontSize: "0.9rem" }} />}
    {...props}
  />
))(({ theme }) => ({
  backgroundColor: "#191a1c",
  color: "white",
  flexDirection: "row",
  fontWeight: 100,
  "& .MuiAccordionSummary-expandIconWrapper.Mui-expanded": {
    transform: "rotate(90deg)"
  },
  "& .MuiAccordionSummary-content": {
    marginLeft: theme.spacing(1)
  },
  "& .MuiAccordionSummary-expandIconWrapper": {
    color: "white"
  }
}));

const AccordionDetails = styled(MuiAccordionDetails)(({ theme }) => ({
  padding: theme.spacing(2),
  borderTop: "1px solid rgba(0, 0, 0, .125)"
}));

const UserReservations = ({ history }) => {
  const [users, setUsers] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const getAllReservations = async () => {
      try {
        const reservations = await getReservations();
        setUsers(reservations.data);
      } catch (ex) {
        if (ex.response) {
          if (ex.response.status === 404) {
            setError(ex.response.data.message);
          } else {
            setError(JSON.stringify(ex.response.data));
          }
          setUsers([]);
        }
      } finally {
        setLoading(false);
      }
    };
    getAllReservations();
  }, []);

  const [expanded, setExpanded] = useState("panel1");

  const handleChange = panel => (event, newExpanded) => {
    setExpanded(newExpanded ? panel : false);
  };
  if (loading) {
    return <Loading />;
  }
  const renderErrorMessage = message => {
    return (
      <div
        style={{
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          height: "100%"
        }}
      >
        <h1 style={{ fontWeight: "400" }}>
          There are no users' reseravtions in the database!
        </h1>
      </div>
    );
  };
  if (error) {
    renderErrorMessage();
  }

  return (
    <div>
      <div className="user-reservation-container">
        {users.length === 0 ? (
          renderErrorMessage()
        ) : (
          <>
            {users.map((user, index) => {
              if (user.reservations.length === 0) return null;
              return (
                <Accordion
                  expanded={expanded === `${index}`}
                  onChange={handleChange(`${index}`)}
                  key={index}
                >
                  <AccordionSummary
                    aria-controls="panel1d-content"
                    id="panel1d-header"
                  >
                    <div className="user-reservations-grid">
                      <span>{user.email}</span>
                      <span>{`${user.first_name} ${user.last_name}`}</span>
                      <span>{user.phone_number}</span>
                      <span>{user.reservations.length}</span>
                    </div>
                  </AccordionSummary>
                  <AccordionDetails>
                    <div>
                      <ReservationsList
                        userReservations={user.reservations}
                        users={users}
                        setUsers={setUsers}
                        key={index}
                        history={history}
                        setError={setError}
                        userId={user.user_id}
                      />
                    </div>
                  </AccordionDetails>
                </Accordion>
              );
            })}
          </>
        )}
      </div>
    </div>
  );
};

export default UserReservations;

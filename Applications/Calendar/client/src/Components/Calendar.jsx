import React, { useRef, useState } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import AddEventModal from "./AddEventModal";
import axios from "axios";
import moment from "moment";


export default function () {

    const [modalOpen, setModalOpen] = useState(false);
    const [events , setEvents] = useState([]);
    const calendarRef = useRef(null);
    const onEventAdded = event => {
        let calendarApi = calendarRef.current.getApi();
        calendarApi.addEvent({
            start: moment(event.start).toDate(),
            end: moment(event.end).toDate(),
            title: event.title
        });
    }

    async function handleEventAdd(data) {
        await axios.post('http://localhost:8080/create-event', data.event);
    }

    async function handleDatesSet(data) {
        const response = await axios.get('http://localhost:8080/?start='+
        moment(data.start).toISOString()+
        '&end='+
        moment(data.end).toISOString());
        setEvents(response.data);
    }

    return (
        <div>
            <div className="text-white p-5 h-10 w-100 bg-black">
                <FullCalendar
                    ref={calendarRef}
                    events={events}
                    plugins={[dayGridPlugin]}
                    initialView="dayGridMonth"
                    datesSet={(date)=>handleDatesSet(date)}
                >
                </FullCalendar>
                    
            </div>   
            <div>
            </div>         
        </div>
    );

}
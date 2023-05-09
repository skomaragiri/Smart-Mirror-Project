import { useState } from "react"

const Clock = () => {
    let time = new Date().toLocaleTimeString();
    let day =  new Date().toLocaleDateString();
    const [ currentTime, setCurrentTime] = useState(time);
    const [ currentDay, setCurrentDay] = useState(day);

    const updateTime = () => {
        let time = new Date().toLocaleTimeString();
        setCurrentTime(time);
    }

    const updateDay = () => {
        let time = new Date().toLocaleDateString();
        setCurrentDay(day);
    }

    setInterval(updateTime, 1000);
    setInterval(updateDay, 1000);


    return (
        <div class="absolute top-4 right-5 h-auto w-auto">
            <div className="text-white text-7xl tabular-nums">
                {currentTime}
            </div>
            <div className="text-white text-5xl tabular-nums text-center">
                {currentDay}
            </div>
        </div>
    )
}

export default Clock;
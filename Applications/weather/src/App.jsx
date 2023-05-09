import TopButtons from "./components/TopButtons";
import Inputs from "./components/Inputs";
import TimeAndLocation from "./components/TimeAndLocation";
import TemperatureAndDetails from "./components/TemperatureAndDetails";
import Forecast from "./components/Forecast";
import getFormattedWeatherData from "./services/weatherService";
import { useEffect, useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {readTextFile, BaseDirectory} from "@tauri-apps/api/fs";
import axios from 'axios';
function App() {
  var latitude = null;
  var longitude = null;
  const fileContent = readTextFile('latitude.txt', { dir: BaseDirectory.Desktop });
  const fileContentone = readTextFile('longitude.txt', { dir: BaseDirectory.Desktop });
  const [query, setQuery] = useState({ q: fileContent });
  const [units, setUnits] = useState("imperial");
  const [weather, setWeather] = useState(null);
  useEffect(() => {
    fileContent.then((result) => {  
      latitude = parseFloat(result);
      var i = 0;
      fileContentone.then((res) => { longitude = parseFloat(res);
        const fetchWeather = async () => {
          await getFormattedWeatherData(latitude, longitude, units).then((data) => {
            setWeather(data);
          });
        };
        fetchWeather();
      });
    });
    // const fetchWeather = async () => {
    //   await getFormattedWeatherData(fileContent, fileContentone, units).then((data) => {
    //     setWeather(data);
    //   });
    // };
    // fetchWeather();
  }, [query, units]);
  return (
    
    <div className="mx-auto max-wscreen-md mt-4 py-5 px-32 bg-black">
      {/* <TopButtons setQuery={setQuery} />
      <Inputs setQuery={setQuery} units={units} setUnits={setUnits} /> */}

      {weather && (
        <div>
          <TimeAndLocation weather={weather} />
          <TemperatureAndDetails weather={weather} />

          <Forecast title="hourly forecast" items={weather.hourly} />
          <Forecast title="daily forecast" items={weather.daily} />
        </div>
      )}
    </div>
  );
}

export default App;

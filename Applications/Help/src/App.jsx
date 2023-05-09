import { useState } from "react";
import reactLogo from "./assets/react.svg";
import { invoke } from "@tauri-apps/api/tauri";
import { BuildingOffice2Icon, CalendarDaysIcon, ChatBubbleLeftEllipsisIcon, ListBulletIcon, MagnifyingGlassCircleIcon, RadioIcon, SparklesIcon } from "@heroicons/react/24/solid";
import "./App.css";




function App() {

  return (
    <div className="flex h-screen justify-center items-center">
      <div class="box text-white bg-gray-700 rounded-lg div-8 p-5 w-4/12">
      <ChatBubbleLeftEllipsisIcon className="h-5 w-5"/>       
        <div class="flex items-center">
          <h2>Hi, Marvis here. Hope you're having a wonderful day. Let me know how I can help you today.</h2>
        </div>
        <div className="indent-1 p-5">
          <p>Try one of the following:</p>
        </div>
        <div className="grid grid-rows-6 gap-2">
          <div className="bg-slate-900 rounded-lg p-4 flex items-center indent-1">
            <BuildingOffice2Icon className="h-5 w-5"/>
            <p>Ask about the weather or forecast in a city</p>
            </div>
          <div className="bg-slate-900 rounded-lg p-4 flex items-center indent-1">
            <CalendarDaysIcon className="h-5 w-5"/>
            <p>Get date and time or add events to your calendar</p>
          </div>
          <div className="bg-slate-900 rounded-lg p-4 flex items-center indent-1">
            <ListBulletIcon className="h-5 w-5"/>
            <p>Edit a list of reminders</p>
          </div>
          <div className="bg-slate-900 rounded-lg p-4 flex items-center indent-1">
            <RadioIcon className="h-5 w-5"/>
            <p>Get current events</p>
          </div>
          <div className="bg-slate-900 rounded-lg p-4 flex items-center indent-1">
            <SparklesIcon className="h-5 w-5"/>
            <p>Tell Jokes</p>
          </div>

          <div className="bg-slate-900 rounded-lg p-4 flex items-center indent-1">
            <MagnifyingGlassCircleIcon className="h-5 w-5"/>
            <p>Search Wikipedia</p>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;

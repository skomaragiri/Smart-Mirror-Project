<dl>
 <dt>Abstract:</dt> 
 <br/>
<dd>Marvis is a modular smart mirror geared towards the everyday homeowner and acts as a productivity tool. It includes functionalities such as providing weather information, calendar reminders, and web searching, all while allowing you to see yourself in the mirror. The text and pictures are displayed through the one-way mirror as only the light can pass through, but the surface of the mirror remains reflective. Marvis is a fully speech-controlled mirror. That means that you can easily navigate the apps on the smart mirror without creating any fingerprint smudges on the physical mirror. </dd>
</dl>
 
<dl>
 <dt>Background:</dt>
 <br/>
 <dd>The advent of smart home devices has revolutionized the way people interact with technology, and the concept of a smart mirror is no exception. A smart mirror is a device that combines a mirror's functionality with technology that can display computer text 
 and images. It allows users to see their reflection while also displaying information such as news, weather, and calendar events on the mirror's surface. The technology is achieved by using a two-way mirror with the correct reflectivity, which enables light to 
 pass through one side of the glass while reflecting light on the other side. The side that is brighter will let light shine through the glass, displaying the computer text and images on the mirror's surface. Although the idea of a smart mirror is not new, it is 
 still not widely available in the market due to a patent held by Hewlett Packard (HP) that expires in 2036. </dd>
 
 <dd>Our smart mirror is designed with cost constraints in mind, which limits its size compared to other smart mirrors on the market. However, it is still an efficient and functional device that fulfills the basic requirements of a smart mirror. We use a 27-inch 
 monitor that is mounted behind a one-way mirror glass with a transparency level of 30%. This monitor has the appropriate brightness to ensure that anything displayed on it that is not black is visible through the mirror. For navigation, most smart mirrors use an 
 infrared (IR) sensor to allow the user to interact with the mirror by touching it; however, we have opted for a voice-controlled smart mirror due to the issues associated with fingerprints on the mirror. </dd>
</dl>

<dl>
 <dt>Operating System:</dt> 
 <br/>
 <dd>Our smart mirror uses the Raspberry Pi 4B microcomputer as its main processing unit. The Raspberry Pi runs EndeavourOS, a Linux distribution for ARM, which is installed on a microSD card using the EndeavourOS ARM image installer found on the x86 version of  
  the OS. We customized the desktop environment to run GNOME, which is further customized to meet our specific needs. The Raspberry Pi is connected to a microphone, which receives voice commands from the user. </dd>
</dl>

<dl>
 <dt>Voice Assistant:</dt> 
 <br/>
 <dd>Our smart mirror uses a voice assistant to provide a hands-free user experience. The voice assistant is programmed to respond to voice commands, which are processed by a microphone embedded in the mirror’s wooden frame. The voice assistant is trained to 
 respond to the wake word "Marvis" and can perform a variety of functions including providing weather updates, setting reminders and appointments, reading the news, and controlling the mirror’s display. </dd>

 <dd>To enable these functions, the voice assistant uses natural language processing (NLP) algorithms and machine learning techniques. Specifically, the voice assistant is built using the Python programming language and utilizes the Bayesian theorem for NLP, which is 
 a probabilistic model that enables the voice assistant to understand and respond to user commands. Additionally, we import the Scikit-learn (sklearn) library which provides efficient tools for data mining and data analysis. Sklearn allows the voice assistant to 
 learn from user interactions and improve its ability to recognize and respond to voice commands over time. <dd>

 <dd>The voice assistant is designed to be customizable, so users can add or remove functions as they see fit. The voice assistant also integrates with other technologies, such as the smart mirror's weather app and task scheduler, which uses MongoDB as the database for storing tasks. Overall, the 
 voice assistant provides a user-friendly and hands-free experience that allows users to interact with the smart mirror without the need for any physical contact. </dd>

 <dd>In addition to the voice recognition capabilities, the smart mirror also utilizes TensorFlow for wake detection. The wake word for the mirror is "Marvis," and the TensorFlow algorithm is trained to detect when the user says the wake word. This feature not only enhances the user experience but 
  also saves energy by not constantly running when it is not in use. </dd>

 <dd>The wake detection algorithm was trained using a dataset of audio clips containing the wake word. The audio clips were annotated to indicate the presence or absence of the wake word. The annotated audio clips were then used to train a Recurrent Neural Network (RNN) to recognize when the 
 user says "Marvis." Once the RNN was trained, it was imported into the smart mirror and integrated into the wake detection system. When the mirror detects the wake word, it will wake up and be ready for voice commands. </dd>
</dl>

<dl>
 <dt>Hardware:</dt> 
 <br/>
 <dd>The Raspberry Pi and microphone are housed in a wooden frame constructed by hand, which also serves as the frame for the mirror. The mirror glass was ordered from a third-party company that provides one-way smart mirror glass with a desired level of transparency of 30% transparent and 70% 
  reflective. The display for the mirror was also purchased and is installed right behind the glass within the wooden frame. The Raspberry Pi is connected to the display and placed out of sight in the frame. The microphone is placed right behind a hole in the frame to take voice input. </dd>
</dl>

<dl>
 <dt>Applications:</dt>
 <br/>
<dd>The smart mirror is equipped with several applications that can be controlled using voice commands. The mirror features a customized front-end built using React.js, which includes a calendar application for scheduling daily tasks and a weather application that displays weather conditions and forecasts. </dd>

<dd>The calendar application allows users to store and manage their daily tasks. The application uses MongoDB as its database to store task data, and CRUD operations are used to maintain the data. The voice assistant is integrated with the calendar application and can manipulate tasks, which are then updated in the front-end application. The front-end is built using React.js, which provides a seamless user interface with a simple and intuitive design. </dd>

<dd>The weather application is another front-end application that is integrated into the smart mirror. The application is built using React.js and is designed to retrieve weather data from the OpenWeather API. This data is then displayed on the mirror's screen for the user to easily access. The weather application has several features that make it stand out. Firstly, the application is designed to display weather data for the user’s current location by default. However, the user also has the option to input a different location to view the weather data for that area. Additionally, the application also displays the temperature, humidity, wind speed, and other weather-related data to give the user a comprehensive understanding of the current weather conditions. Moreover, the weather app can be easily controlled by the voice assistant. Users can simply ask the voice assistant for the current weather conditions or to provide a weather forecast for the day. The voice assistant will then retrieve the relevant data from the OpenWeather API and display it on the screen. Overall, the integration of the weather application into the smart mirror adds to the mirror's functionality and provides users with an easy way to stay up-to-date on the weather conditions. </dd>

<dd>To power the applications, we decided to use Tauri, a lightweight and flexible framework for building native desktop applications using web technologies. Tauri offers several advantages over Electron, which is a popular framework for building cross-platform desktop applications. Tauri uses a much smaller bundle size and offers faster startup times, which is critical for our smart mirror application. Additionally, Tauri offers better security features and a smaller memory footprint, which makes it more suitable for resource-constrained devices like the Raspberry Pi. </dd>

<dd>In addition to the front-end applications, the mirror is equipped with a voice assistant that uses machine-learning algorithms to understand and respond to voice commands. The voice assistant is built using TensorFlow and scikit-learn libraries and is trained using the Bayesian theorem. The wake detection for the voice assistant is done using TensorFlow, which detects the wake word "Marvis." Once the wake word is detected, the voice assistant listens to the command and responds accordingly. The voice assistant can perform several functions, including providing information from Wikipedia, reading out the news, telling the time, date, weather, and managing tasks for the day. </dd>

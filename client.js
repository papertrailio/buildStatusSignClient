require("dotenv").config();

const firebase = require("firebase");
var gpio = require("rpi-gpio");
var gpiop = gpio.promise;

const pins = {
  api1green: 3,
  api1amber: 5,
  api1red: 7,
  api2green: 8,
  api2amber: 10,
  api2red: 11,
  webclient1green: 12,
  webclient1amber: 13,
  webclient1red: 15,
  webclient2green: 16,
  webclient2amber: 18,
  webclient2red: 19,
  ptapp1green: 21,
  ptapp1amber: 22,
  ptapp1red: 23,
  ptapp2green: 24,
  ptapp2amber: 26,
  ptapp2red: 31
};

const initLeds = () =>
  Promise.all(
    Object.keys(keys =>
      keys.forEach(key => {
        console.log("setup pin", pins[key]);
        return gpiop
          .setup(pins[key], gpio.DIR_OUT)
          .then(() => gpiop.write(pins[key], true));
      })
    )
  );

const initStatuses = () => {
  const config = {
    databaseURL: process.env.DATABASE_URL
  };
  firebase.initializeApp(config);

  return firebase.database().ref("/statuses");
};

const setLeds = console.log;

// gpiop
//   .setup(8, gpio.DIR_OUT)
//   .then(() => {
//     return gpiop.write(8, true);
//   })
//   .catch(err => {
//     console.log("Error: ", err.toString());
//   });

// gpiop
//   .setup(7, gpio.DIR_OUT)
//   .then(() => {
//     return gpiop.write(7, true);
//   })
//   .catch(err => {
//     console.log("Error: ", err.toString());
//   });

// gpiop
//   .setup(5, gpio.DIR_OUT)
//   .then(() => {
//     return gpiop.write(5, false);
//   })
//   .catch(err => {
//     console.log("Error: ", err.toString());
//   });
// gpiop
//   .setup(3, gpio.DIR_OUT)
//   .then(() => {
//     return gpiop.write(3, false);
//   })
//   .catch(err => {
//     console.log("Error: ", err.toString());
//   });

initLeds().then(() => {
  const statuses = initStatuses();

  statuses.on("value", snapshot => setLeds(snapshot.val()));
});

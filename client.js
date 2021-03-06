require("dotenv").config();

const firebase = require("firebase");
var gpio = require("rpi-gpio");
var gpiop = gpio.promise;

const pins = {
  api1green: 3,
  api1amber: 5,
  api1red: 8,
  api2green: 10,
  api2amber: 11,
  api2red: 12,
  webclient1green: 13,
  webclient1amber: 15,
  webclient1red: 16,
  webclient2green: 18,
  webclient2amber: 19,
  webclient2red: 21,
  ptapp1green: 23,
  ptapp1amber: 24,
  ptapp1red: 26,
  ptapp2green: 35,
  ptapp2amber: 36,
  ptapp2red: 37
};

const initLeds = () =>
  Promise.all(
    Object.keys(pins).map((key, index) => {
      console.log("setup", pins[key]);
      return gpiop.setup(pins[key], gpio.DIR_OUT).then(() => {
        console.log("write", pins[key], false);
        gpiop.write(pins[key], false);
        setTimeout(() => {
          console.log("write", pins[key], true);
          gpiop.write(pins[key], true);
        }, 1000 * index);
      });
    })
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

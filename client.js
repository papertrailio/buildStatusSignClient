require("dotenv").config();

const firebase = require("firebase");
var gpio = require("rpi-gpio");
var gpiop = gpio.promise;

const pins = {
  api1red: 3,
  api1amber: 5,
  api1green: 7,
  api2red: 8,
  api2amber: 10,
  api2green: 11,
  webclient1red: 12,
  webclient1amber: 13,
  webclient1green: 15,
  webclient2red: 16,
  webclient2amber: 18,
  webclient2green: 19,
  ptapp1red: 21,
  ptapp1amber: 22,
  ptapp1green: 23,
  ptapp2red: 24,
  ptapp2amber: 26,
  ptapp2green: 31
};

const initLeds = () => Promise.resolve();
Promise.all(
  Object.keys(keys =>
    keys.forEach(key => {
      gpiop.setup(pins[key], gpio.DIR_OUT);
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

initLeds().then(() => {
  const statuses = initStatuses();

  statuses.on("value", snapshot => setLeds(snapshot.val()));
});

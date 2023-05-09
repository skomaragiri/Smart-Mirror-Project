const eventModel = require('../models/eventModel');


// module.exports.getEvent = async (req, res) => {
//     const events = await eventModel.find()
//     res.send(events)
// }

// module.exports.saveEvent = async (req, res) => {
//     const {text,date} = req.body;
//     eventModel
//     .create({text, date})
//     .then((data) => {
//         console.log("added succesfully");
//         console.log(data);
//         res.send(data)
//     })
// }

// module.exports.updateEvent = async (req, res) => {
//     const {_id, text, date} = req.body;
//     eventModel
//     .findByIdAndUpdate(_id, {text}, {date})
//     .then(() => res.send("updated succesfully"))
//     .catch((err) => console.log(err))
// }

// module.exports.deleteEvent = async (req, res) => {
//     const {_id } = req.body;
//     eventModel
//     .findByIdAndDelete(_id)
//     .then(() => res.send("deleted succesfully"))
//     .catch((err) => console.log(err))
// }

const moment = require('moment');

module.exports.createEvent = async(req, res) => {
    const event = eventModel(req.body);
    await event.save();
    res.sendStatus(201);
};

module.exports.getEvent = async(req, res) => {
    const events = await eventModel.find({
        start: {$gte: moment(req.query.start).toDate()}, 
        end: {$lte: moment(req.query.end).toDate()}
    });

    res.send(events);
};

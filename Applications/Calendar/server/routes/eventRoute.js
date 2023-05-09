const {Router} = require('express');
const { getEvent, createEvent } = require('../controllers/eventController');

const router = Router();

router.get('/', getEvent)
router.post('/create-event', createEvent)
// router.post('/update', updateEvent)
// router.post('/delete', deleteEvent)
module.exports = router;
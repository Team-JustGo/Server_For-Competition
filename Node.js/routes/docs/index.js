const express = require('express');
const router = express.Router();

const pathToSwaggerUi = require('swagger-ui-dist').absolutePath();

router.get('/', (req, res) => res.redirect('/api/docs/swagger-ui?url=/docs/api-spec.json'));
router.use('/swagger-ui', express.static(pathToSwaggerUi));
router.use('/api-spec.json', express.static('../../public/api-spec.json'));

module.exports = router;
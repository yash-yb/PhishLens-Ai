const express = require('express');
const cors = require('cors');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 5000;
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';

// Supabase Init (Optional for prototype)
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;
const supabase = (supabaseUrl && !supabaseUrl.includes('your-project')) ? createClient(supabaseUrl, supabaseKey) : null;

app.use(cors());
app.use(express.json());

// Multer setup
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

app.get('/', (req, res) => {
    res.send('PhishLens AI API Gateway (Local Prototype Mode)');
});

app.post('/api/scan', upload.single('image'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No image provided' });
        }

        console.log(`Processing image: ${req.file.originalname}`);

        // Forward directly to ML Service
        const form = new FormData();
        form.append('file', req.file.buffer, {
            filename: req.file.originalname,
            contentType: req.file.mimetype,
        });

        const mlResponse = await axios.post(`${ML_SERVICE_URL}/analyze`, form, {
            headers: form.getHeaders(),
            maxContentLength: Infinity,
            maxBodyLength: Infinity
        });

        res.json({
            success: true,
            ...mlResponse.data
        });

    } catch (error) {
        console.error('Scan Error:', error.response?.data || error.message);
        res.status(500).json({ error: 'Failed to process image. Make sure ML service is active.' });
    }
});

app.listen(port, () => {
    console.log(`API Gateway (Local Mode) running on port ${port}`);
});

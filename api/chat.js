export default async function handler(req, res) {
    // Habilitar CORS por si acaso
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Método no permitido' });
    }

    try {
        const { mensaje } = req.body;

        // Recuperamos la clave secreta guardada de forma segura en Vercel
        const apiKey = process.env.GEMINI_API_KEY;
        
        if (!apiKey) {
            return res.status(500).json({ respuesta: "Error: La API Key no está configurada en el servidor." });
        }

        const CONTEXTO_ASISTENTE = "Sos LucAI, el asistente virtual inteligente de Luca Baldiviezo[cite: 1]. Tu propósito es responder dudas sobre Luca (su carrera, habilidades, gustos) de forma amable, profesional, concisa y con un toque tecnológico moderno[cite: 1]. Si te preguntan algo ajeno a Luca, responde amablemente vinculándolo con él o aclarando tu rol[cite: 1].";

        // Llamamos a los servidores de Google Gemini desde el backend de Vercel
        const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
        
        const response = await fetch(geminiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [{
                    parts: [{ text: `${CONTEXTO_ASISTENTE}\n\nPregunta del usuario: ${mensaje}` }]
                }]
            })
        });

        const data = await response.json();
        const respuestaIA = data.candidates[0].content.parts[0].text;

        // Le devolvemos la respuesta limpia al frontend
        return res.status(200).json({ respuesta: respuestaIA });

    } catch (error) {
        console.error(error);
        return res.status(500).json({ respuesta: "Hubo un problema al procesar tu solicitud en el servidor." });
    }
}

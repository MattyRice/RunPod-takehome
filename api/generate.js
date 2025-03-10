export default async function handler(req, res) {
  try {
    const { prompt, num_inference_steps, guidance_scale, seed } = req.body;
    
    // Access the token from environment variables
    const hfToken = process.env.HF_TOKEN;

    const response = await fetch(`https://api.runpod.ai/v2/${process.env.RUNPOD_ENDPOINT_ID}/run`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.RUNPOD_API_KEY}`
      },
      body: JSON.stringify({
        input: {
          prompt,
          num_inference_steps,
          guidance_scale,
          seed
        }
      })
    });
    
    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

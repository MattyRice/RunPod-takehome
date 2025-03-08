

# FLUX Image Generator

A web application that generates images using the FLUX.1-dev model via RunPod's API.

**Live Demo**: [https://run-pod-takehome.vercel.app](https://run-pod-takehome.vercel.app)

## Features

- Generate images from text prompts
- Customize generation parameters (inference steps, guidance scale, seed)
- View generation history
- Download generated images
- Responsive design for desktop and mobile

## Project Structure

```
├── index.html          # Main frontend interface
├── api/
│   ├── generate.js     # API endpoint for image generation
│   └── status.js       # API endpoint for checking generation status
```

## Local Development Setup

### Prerequisites

- Node.js (v14 or later)
- A RunPod account with API access
- A RunPod endpoint running the FLUX.1-dev model

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/flux-image-generator.git
cd flux-image-generator
```

2. **Install dependencies**

```bash
npm install
```

3. **Create environment variables**

Create a `.env.local` file in the root directory with the following variables:

```
RUNPOD_API_KEY=your_runpod_api_key
RUNPOD_ENDPOINT_ID=your_endpoint_id
```

Replace `your_runpod_api_key` and `your_endpoint_id` with your actual RunPod API key and endpoint ID.

4. **Run the development server**

```bash
npm run dev
```

5. **Open your browser**

Navigate to `http://localhost:3000` to see the application running.

## Deployment to Vercel

1. **Create a Vercel account** at [vercel.com](https://vercel.com) if you don't have one

2. **Install the Vercel CLI**

```bash
npm install -g vercel
```

3. **Deploy to Vercel**

```bash
vercel
```

4. **Set environment variables in Vercel**

After deployment, go to your project settings in the Vercel dashboard and add the following environment variables:

- `RUNPOD_API_KEY`: Your RunPod API key
- `RUNPOD_ENDPOINT_ID`: Your RunPod endpoint ID

5. **Redeploy the application**

```bash
vercel --prod
```

## How It Works

1. The user enters a prompt and optional parameters
2. The frontend sends a request to the `/api/generate` endpoint
3. The backend forwards the request to RunPod's API
4. The frontend periodically checks the status via the `/api/status` endpoint
5. When the image is ready, it's displayed to the user and saved in the history

## Security Considerations

- API keys are stored as environment variables on the server
- No sensitive information is exposed in the client-side code
- Local storage is used to save image history, with limits to prevent exceeding storage quotas

## Limitations

- RunPod's free tier has usage limits
- Large images may not be saved in history due to localStorage limitations
- Generation can take 15-30 seconds depending on server load

import { NextRequest, NextResponse } from 'next/server';

// Try 127.0.0.1 first (better for Next.js server-side), fallback to localhost
const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8000';
const BACKEND_URL_FALLBACK = process.env.BACKEND_URL || 'http://localhost:8000';

// Helper function to try fetching with fallback
async function fetchWithFallback(url: string, fallbackUrl: string, options: RequestInit): Promise<Response> {
  try {
    return await fetch(url, options);
  } catch (error: any) {
    // If first URL fails with connection error, try fallback
    if (error.message?.includes('ECONNREFUSED') || error.message?.includes('fetch failed')) {
      console.warn(`Primary backend URL failed (${url}), trying fallback (${fallbackUrl})`);
      return await fetch(fallbackUrl, options);
    }
    throw error;
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Optional: Quick health check (non-blocking - if it fails, we'll still try the main request)
    // This helps provide better error messages but doesn't block the request
    let backendReachable = false;
    try {
      const healthController = new AbortController();
      const healthTimeout = setTimeout(() => healthController.abort(), 3000); // 3 second timeout
      
      const healthCheck = await fetchWithFallback(
        `${BACKEND_URL}/health`,
        `${BACKEND_URL_FALLBACK}/health`,
        {
          method: 'GET',
          signal: healthController.signal,
          headers: {
            'Accept': 'application/json',
          },
        }
      );
      clearTimeout(healthTimeout);
      
      if (healthCheck.ok) {
        backendReachable = true;
      }
    } catch (healthError: any) {
      // Health check failed - but we'll still try the main request
      console.warn('Backend health check failed (will still attempt main request):', healthError.message);
      backendReachable = false;
    }

    // Forward the request to the Python backend with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 180000); // 180 second timeout (3 minutes for LLM processing)

    try {
      const response = await fetchWithFallback(
        `${BACKEND_URL}/api/match`,
        `${BACKEND_URL_FALLBACK}/api/match`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify(body),
          signal: controller.signal,
          // Ensure we're not caching this request
          cache: 'no-store',
        }
      );

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Backend error:', errorText);
        return NextResponse.json(
          { 
            error: `Backend error: ${response.status}`,
            message: errorText || 'Unknown backend error'
          },
          { status: response.status }
        );
      }

      const data = await response.json();
      return NextResponse.json(data);
    } catch (fetchError: any) {
      clearTimeout(timeoutId);
      
      if (fetchError.name === 'AbortError') {
        return NextResponse.json(
          { 
            error: 'Request timeout',
            message: 'The backend took too long to respond. Please try again.'
          },
          { status: 504 }
        );
      }
      
      // Connection error - provide detailed error message
      const isConnectionError = fetchError.message?.includes('ECONNREFUSED') || 
          fetchError.message?.includes('fetch failed') ||
          fetchError.message?.includes('ECONNREFUSED') ||
          fetchError.cause?.code === 'ECONNREFUSED' ||
          fetchError.code === 'ECONNREFUSED' ||
          (fetchError.message && fetchError.message.includes('connect'));
      
      if (isConnectionError) {
        console.error('Connection error details:', {
          message: fetchError.message,
          cause: fetchError.cause,
          code: fetchError.code,
          backendUrl: BACKEND_URL,
          backendReachable: backendReachable
        });
        
        const errorMessage = backendReachable 
          ? `Connection error occurred. Backend was reachable but the request failed. Please check the backend logs.`
          : `Unable to connect to the matching service at ${BACKEND_URL}. Please make sure the Python backend is running on port 8000. Run: cd backend && python3 main.py`;
        
        return NextResponse.json(
          { 
            error: 'Connection refused',
            message: errorMessage
          },
          { status: 503 }
        );
      }
      
      throw fetchError; // Re-throw to be caught by outer catch
    }
  } catch (error: any) {
    console.error('Error proxying to backend:', error);
    return NextResponse.json(
      { 
        error: `Failed to connect to backend: ${error.message}`,
        message: 'Unable to connect to the matching service. Please make sure the Python backend is running on port 8000.'
      },
      { status: 500 }
    );
  }
}


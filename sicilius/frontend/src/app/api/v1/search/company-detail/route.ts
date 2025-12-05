import { NextRequest, NextResponse } from 'next/server';

const BACKEND_ORIGIN =
  process.env.BACKEND_ORIGIN ||
  (process.env.NODE_ENV === 'development'
    ? 'http://localhost:5001'
    : 'https://api.sicilius.com.tr');

export const runtime = 'nodejs';

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);
  const companyId = requestUrl.searchParams.get('company_id');

  if (!companyId) {
    return NextResponse.json({ detail: 'company_id is required' }, { status: 422 });
  }

  const backendUrl = `${BACKEND_ORIGIN}/api/v1/search/company-detail?company_id=${encodeURIComponent(
    companyId,
  )}`;

  const headers = new Headers();
  headers.set('accept', 'application/json');
  const cookieHeader = request.headers.get('cookie');
  if (cookieHeader) {
    headers.set('cookie', cookieHeader);
  }

  let backendResponse: Response;
  try {
    backendResponse = await fetch(backendUrl, {
      method: 'GET',
      headers,
      cache: 'no-store',
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    return NextResponse.json(
      {
        detail: 'Backend request failed',
        error: message,
      },
      { status: 502 },
    );
  }

  const proxiedHeaders = new Headers(backendResponse.headers);
  proxiedHeaders.delete('content-encoding');
  proxiedHeaders.delete('transfer-encoding');
  proxiedHeaders.delete('content-length');

  return new NextResponse(backendResponse.body, {
    status: backendResponse.status,
    headers: proxiedHeaders,
  });
}

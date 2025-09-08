import { NextResponse } from 'next/server';

export async function POST(request) {
  try {
    const body = await request.json();
    // Your chat logic here
    return NextResponse.json({ answer: "response" });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
} 
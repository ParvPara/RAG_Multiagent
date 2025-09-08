import { NextResponse } from 'next/server';

export async function DELETE(request, { params }) {
  try {
    const { filename } = params;
    // Your delete logic here
    return NextResponse.json({ message: `File ${filename} deleted successfully` });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
} 
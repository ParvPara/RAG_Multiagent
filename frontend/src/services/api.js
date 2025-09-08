const API_URL = process.env.NEXT_PUBLIC_API_URL;
if (!API_URL) {
  console.error('NEXT_PUBLIC_API_URL environment variable is not set!');
}
console.log('Using API URL:', API_URL);

export const api = {
  async getDocuments() {
    try {
      const url = `${API_URL}/documents`;
      console.log('Fetching documents from:', url);
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const data = await response.json();
      console.log('Documents received:', data);
      return data;
    } catch (error) {
      console.error('Error fetching documents:', error);
      throw error;
    }
  },

  async uploadDocument(file) {
    try {
      console.log('Uploading file:', file.name);
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch(`${API_URL}/documents/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Upload error response:', errorText);
        throw new Error(`Upload failed: ${response.status}, details: ${errorText}`);
      }

      const data = await response.json();
      console.log('Upload response:', data);
      return data;
    } catch (error) {
      console.error('Upload error:', error);
      throw error;
    }
  },

  async sendQuestion(question) {
    try {
      console.log('Sending question:', question);
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Chat failed: ${response.status}, details: ${errorText}`);
      }

      const data = await response.json();
      console.log('Answer received:', data);
      return data;
    } catch (error) {
      console.error('Chat error:', error);
      throw error;
    }
  },

  async deleteDocument(filename) {
    try {
      const response = await fetch(`${API_URL}/documents/${filename}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Delete failed: ${response.status}, details: ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Delete error:', error);
      throw error;
    }
  },
}; 
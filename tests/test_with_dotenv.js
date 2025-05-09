// Import the dotenv package to load environment variables from .env file
require('dotenv').config();

// Function to test API keys
async function testAPIKeys() {
  console.log('\x1b[36m%s\x1b[0m', '=== Testing API Keys ===');
  
  // Check if API keys are loaded
  const veniceApiKey = process.env.VENICE_API_KEY;
  const geminiApiKey = process.env.GEMINI_API_KEY;
  
  console.log(`Venice API key length: ${veniceApiKey ? veniceApiKey.length : 0}`);
  console.log(`Gemini API key length: ${geminiApiKey ? geminiApiKey.length : 0}`);
  
  if (!veniceApiKey || !geminiApiKey) {
    console.error('\x1b[31m%s\x1b[0m', 'Error: API keys not found in environment variables');
    console.log('Make sure you have a .env file with VENICE_API_KEY and GEMINI_API_KEY defined');
    return;
  }
  
  try {
    // Test Venice API - Models List
    console.log('\n\x1b[36m%s\x1b[0m', '=== Testing Venice API - Models List ===');
    const veniceModelsResponse = await fetch('https://api.venice.ai/api/v1/models', {
      headers: {
        'Authorization': `Bearer ${veniceApiKey}`
      }
    });
    
    const veniceModelsData = await veniceModelsResponse.json();
    console.log('Status:', veniceModelsResponse.status);
    
    if (veniceModelsResponse.ok) {
      console.log('First model:', veniceModelsData.data?.[0]?.id || 'No models found');
    } else {
      console.error('Error:', veniceModelsData);
    }
    
    // Test Venice API - Chat Completion
    console.log('\n\x1b[36m%s\x1b[0m', '=== Testing Venice API - Chat Completion ===');
    const veniceChatResponse = await fetch('https://api.venice.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${veniceApiKey}`
      },
      body: JSON.stringify({
        model: 'llama-3.2-3b',
        messages: [{ role: 'user', content: 'Hello, can you tell me what day it is today?' }],
        temperature: 0.7
      })
    });
    
    const veniceChatData = await veniceChatResponse.json();
    console.log('Status:', veniceChatResponse.status);
    
    if (veniceChatResponse.ok) {
      console.log('Response:', veniceChatData.choices?.[0]?.message?.content || 'No response content');
    } else {
      console.error('Error:', veniceChatData);
    }
    
    // Test Gemini API - Models List
    console.log('\n\x1b[36m%s\x1b[0m', '=== Testing Gemini API - Models List ===');
    const geminiModelsResponse = await fetch(`https://generativelanguage.googleapis.com/v1/models?key=${geminiApiKey}`);
    
    const geminiModelsData = await geminiModelsResponse.json();
    console.log('Status:', geminiModelsResponse.status);
    
    if (geminiModelsResponse.ok) {
      console.log('Models count:', geminiModelsData.models?.length || 0);
    } else {
      console.error('Error:', geminiModelsData);
    }
    
    // Test Gemini API - Chat Completion
    console.log('\n\x1b[36m%s\x1b[0m', '=== Testing Gemini API - Chat Completion ===');
    const geminiChatResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=${geminiApiKey}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        contents: [
          {
            parts: [
              { text: 'Hello, can you tell me what day it is today?' }
            ]
          }
        ]
      })
    });
    
    const geminiChatData = await geminiChatResponse.json();
    console.log('Status:', geminiChatResponse.status);
    
    if (geminiChatResponse.ok) {
      console.log('Response:', geminiChatData.candidates?.[0]?.content?.parts?.[0]?.text || 'No response content');
    } else {
      console.error('Error:', geminiChatData);
    }
    
  } catch (error) {
    console.error('\x1b[31m%s\x1b[0m', 'Error during API tests:', error.message);
  }
}

// Run the tests
testAPIKeys();
// Test API connectivity directly
async function testSearchAPI() {
    console.log('🧪 Testing Search API...');
    
    try {
        const response = await fetch('http://127.0.0.1:7000/search_jobs?keyword=product&location=india');
        const data = await response.json();
        
        console.log('✅ API Test Success:', data);
        return data;
    } catch (error) {
        console.error('❌ API Test Failed:', error);
        throw error;
    }
}

// Test axios specifically
async function testAxiosAPI() {
    console.log('🧪 Testing Axios API...');
    
    try {
        const response = await axios.get('http://127.0.0.1:7000/search_jobs', {
            params: {
                keyword: 'product',
                location: 'india'
            }
        });
        
        console.log('✅ Axios Test Success:', response.data);
        return response.data;
    } catch (error) {
        console.error('❌ Axios Test Failed:', error);
        throw error;
    }
}

// Make tests available globally
window.testSearchAPI = testSearchAPI;
window.testAxiosAPI = testAxiosAPI;

console.log('🔧 API Test functions loaded. Use testSearchAPI() or testAxiosAPI() in console.');
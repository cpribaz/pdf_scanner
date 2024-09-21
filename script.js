document.getElementById('pdf-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('pdf', document.getElementById('pdf-file').files[0]);
    formData.append('keywords', document.getElementById('keywords').value);

    try {
        const response = await fetch('http://127.0.0.1:5000/scan-pdf', { 
            method: 'POST',
            body: formData
        });
        

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
    }
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (data.results.length > 0) {
        data.results.forEach(result => {
            const resultDiv = document.createElement('div');
            resultDiv.innerHTML = `<p>Keyword: ${result.keyword}, Page: ${result.page}, Excerpt: ${result.excerpt}</p>`;
            resultsDiv.appendChild(resultDiv);
        });
    } else {
        resultsDiv.innerHTML = '<p>No keywords found.</p>';
    }
}


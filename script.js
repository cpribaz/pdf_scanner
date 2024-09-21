document.getElementById('pdf-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const pdfFile = document.getElementById('pdf-file').files[0];
    const keywords = document.getElementById('keywords').value;

    if (!pdfFile || !keywords) {
        alert('Please upload a PDF and enter keywords.');
        return;
    }

    // Create form data to send to backend
    const formData = new FormData();
    formData.append('pdf', pdfFile);
    formData.append('keywords', keywords);

    // Send request to backend
    const response = await fetch('/scan-pdf', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();

    // Display results
    displayResults(result);
});

function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    if (result.error) {
        resultsDiv.textContent = result.error;
        return;
    }

    result.forEach((entry) => {
        const div = document.createElement('div');
        div.innerHTML = `<strong>Keyword:</strong> ${entry.keyword}<br>
                        <strong>Page:</strong> ${entry.page}<br>
                        <strong>Excerpt:</strong> ${entry.excerpt}`;
        resultsDiv.appendChild(div);
    });
}

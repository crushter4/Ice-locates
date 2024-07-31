document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('myForm');
    const submissionsDiv = document.getElementById('submissions');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = new URLSearchParams(formData);

        fetch('/', {
            method: 'POST',
            body: data
        })
        .then(response => response.json())
        .then(result => {
            alert(result.message);
            form.reset();
            loadSubmissions();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function loadSubmissions() {
        fetch('/get_submissions')
        .then(response => response.json())
        .then(submissions => {
            submissionsDiv.innerHTML = '<h2>Submissions</h2>';
            submissions.forEach(sub => {
                submissionsDiv.innerHTML += `<p>${sub[1]} (${sub[2]}): ${sub[3]}</p>`;
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Load submissions when the page loads
    loadSubmissions();
});

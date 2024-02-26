const fileInput = document.getElementById('zip-file');
fileInput.addEventListener('change', updateDescription);
function updateDescription() {
    const selectedFile = fileInput.files[0];
    const descriptionSpan = document.getElementById('file-description');
    
    // Check if a file is selected
    if (selectedFile) {
        // Check if the file is a .zip file
        if (selectedFile.name.toLowerCase().endsWith('.zip')) {
            descriptionSpan.textContent = selectedFile.name;
        } else {
            alert('Please select a .zip file.');
            fileInput.value = '';  // Clear the input field
            descriptionSpan.textContent = '';
        }
    } else {
        // Clear the description if no file is selected
        descriptionSpan.textContent = '';
    }
}

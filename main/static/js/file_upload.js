const ALLOWED_FILE_SIZE = 128;
const fileInput = document.getElementById('zip-file');
fileInput.addEventListener('change', handleFileInputChange);
function handleFileInputChange() {
    const selectedFile = fileInput.files[0];
    const descriptionSpan = document.getElementById('file-description');
    
    if (selectedFile) {
        if (selectedFile.name.toLowerCase().endsWith('.zip')) {
            const fileSizeMB = selectedFile.size / (1000 * 1000);
            if (fileSizeMB > ALLOWED_FILE_SIZE) {
                document.getElementById('messages')?.remove();
                document.querySelector('.modal-title').insertAdjacentHTML('afterend',`
                    <div id="messages">
                        <ul>
                            <li>File size exceeds ${ALLOWED_FILE_SIZE}MB. Please select a smaller file.</li>
                        </ul>
                    </div>
                `);
                fileInput.value = '';
                descriptionSpan.textContent = '';
                return;
            }
            descriptionSpan.textContent = selectedFile.name;
        } else {
            alert('Please select a .zip file.');
            fileInput.value = '';
            descriptionSpan.textContent = '';
        }
    } else {
        descriptionSpan.textContent = '';
    }
}

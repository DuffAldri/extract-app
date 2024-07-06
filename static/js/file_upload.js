// Required elements
const uploadArea = document.querySelector('#upload-area');
const fileUploadForm = document.querySelector('#file-upload-form');
const filenameDiv = document.querySelector('#filename-div');
let fileInput = document.querySelector('#file-input');
let chooseFileButton = document.querySelector('#choose-file-button');
let verifiedFile;

chooseFileButton.addEventListener('click', () => { 
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    let file = fileInput.files[0];
    checkFile(file);
});

uploadArea.addEventListener("dragover", (event)=>{
    event.preventDefault();
    console.log('File is over upload-area');
    uploadArea.classList.add("active");

});

uploadArea.addEventListener("dragleave", ()=>{
    console.log('Dragleave');
    uploadArea.classList.remove("active");

});

uploadArea.addEventListener("drop", (event)=>{
    event.preventDefault();
    console.log('File is dropped');
    uploadArea.classList.remove("active");
    let file = event.dataTransfer.files[0];

    checkFile(file);

});

filenameDiv.querySelector("a").addEventListener("click", function(event) {
    event.preventDefault();

    fileInput.value = '';
    verifiedFile = '';
    addFilenameText(false);
});

document.querySelectorAll('.submit-button').forEach(button=>{
    button.addEventListener("click", function(event) {
        event.preventDefault();
        if (verifiedFile) {
            const formData = new FormData();
            formData.append('file', verifiedFile);
            formData.append('algorithm', this.value);

            // // Submit the form data using fetch or XMLHttpRequest
            // fetch(fileUploadForm.action, {
            //     method: 'POST',
            //     body: formData,
            // })
            // .then(data => {
            //     console.log('Success:', data);
            //     alert('File uploaded successfully!');                
            //     if (data.url) {
            //         // window.location.href = data.url;
            //     }
            // })
            // .catch((error) => {
            //     console.error('Error:', error);
            //     alert('Failed to upload file.');
            // });


            // Send the FormData object using fetch
            fetch(fileUploadForm.action, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                // Check if response is not ok (status not 200-299)
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.error);
                    });
                } else {
                    console.log('Success:', response);
                    
                    fileInput.value = '';
                    verifiedFile = '';
                    if (response.url) {
                        window.location.href = response.url;
                    }
                }
            })
            // .then(data => {
            //     console.log('Success:', data);
            //     alert('File uploaded successfully!');
            //     // if (data.url) {
            //     //     window.location.href = data.url;
            //     // }
            // })
            .catch(error => {
                console.error('Error:', error.message);
                
                addFilenameText(false);
                fileInput.value = '';
                verifiedFile = '';
                uploadArea.classList.add("error");
                alert('Gagal: ' + error.message);
            });
        } else {
            alert('Please select a valid file before submitting.');
        }
    });
});

function checkFile(file) {
    fileExtension = file.name.split('.').pop().toLowerCase();
    let validExtension = ["xlsx", "xls"]

    if(!validExtension.includes(fileExtension)) {
        alert(`File yang diunggah tidak berekstensi .xls atau .xlsx: ${file.name}`)
        uploadArea.classList.add("error");

        fileInput.value = '';
        verifiedFile = '';
        addFilenameText(false);
    } else {
        uploadArea.classList.remove("error");
        addFilenameText(file.name)
        verifiedFile = file;
        console.log(verifiedFile);
    }
}

function addFilenameText(filename) {
    if(filename == false) {
        filenameDiv.classList.remove('show');
    } else {
        filenameDiv.classList.add('show');
        
        filenameDiv.querySelector('p').textContent = "Uploaded File: " + filename

    }
}

function checkTemplate(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = function(event) {
            try {
                const data = new Uint8Array(event.target.result);
                const workbook = XLSX.read(data, { type: 'array' });
                const firstSheetName = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[firstSheetName];

                // Check if A1 is 'review'
                const cellA1 = worksheet['A1'];
                if (cellA1 && cellA1.v === 'review') {
                    console.log("A1 is 'review'");

                    // Check if column A after A1 is empty or not
                    let isEmpty = true;
                    for (let row = 2; worksheet['A' + row]; row++) {
                        const cell = worksheet['A' + row];
                        if (cell && cell.v.trim() !== '') {
                            isEmpty = false;
                            break;
                        }
                    }
                    if (isEmpty) {
                        resolve("empty");
                    } else {
                        resolve("success");
                    }
                } else {
                    resolve("template");
                }
            } catch (error) {
                reject(error);
            }
        };
        reader.onerror = function(error) {
            reject(error);
        };
        reader.readAsArrayBuffer(file);
    });
}
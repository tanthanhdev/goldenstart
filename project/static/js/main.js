
$(document).ready(function(){
    let cookie = document.cookie
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)

    let uploadButton = document.getElementById("input-file");
    let container = document.querySelector(".content-upload");
    //let error = document.getElementById("error");
    let imageDisplay = document.getElementById("image-display");

    var email = ""

    // Increment the visit counter
    axios({
        method: "POST",
        url: "/post-visited", 
        headers: {
          'X-CSRFToken': csrfToken
        },
    })
    .then(console.log("visited incremented"))
    .catch(error => console.log(error))


    $('#additive').on('submit', function(e) {
        e.preventDefault();
        email = $("#additive-email").val();
        data = $(this).serialize();

        $.ajax({
            type: "POST",
            url: '/subscribe',
            data: data,
            success: function(data) {
                $('#additive').addClass('d-none');
                $('.container-upload').removeClass('d-none');
            },
            error: function(data) {
            }
        }); 
    })


    //Upload Button
    if (uploadButton) {
        uploadButton.addEventListener("change", () => {
            imageDisplay.innerHTML = "";
            Array.from(uploadButton.files).forEach((file) => {
                fileHandler(file, file.name, file.type);
            });
        });
    }
    
    container.addEventListener(
        "dragenter",
        (e) => {
        e.preventDefault();
        e.stopPropagation();
        container.classList.add("active");
        },
        false
    );
    
    container.addEventListener(
        "dragleave",
        (e) => {
        e.preventDefault();
        e.stopPropagation();
        container.classList.remove("active");
        },
        false
    );
    
    container.addEventListener(
        "dragover",
        (e) => {
        e.preventDefault();
        e.stopPropagation();
        container.classList.add("active");
        },
        false
    );
    
    container.addEventListener(
        "drop",
        (e) => {
        e.preventDefault();
        e.stopPropagation();
        container.classList.remove("active");
        let draggedData = e.dataTransfer;
        let files = draggedData.files;
        imageDisplay.innerHTML = "";
        Array.from(files).forEach((file) => {
            fileHandler(file, file.name, file.type);
        });
        },
        false
    );


    const fileHandler = (file, name, type) => {
        // if (type.split("/")[0] !== "image") {
        //     //File Type Error
        //     error.innerText = "Please upload an image file";
        //     return false;
        // }
        //     error.innerText = "";
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
            //image and file name
            let imageContainer = document.createElement("figure");
            imageContainer.innerHTML += `<figcaption>${name}</figcaption>`;
            imageDisplay.appendChild(imageContainer);

            // Call api file upload function
            let form_data = new FormData();
            form_data.append("file", file);
            form_data.append("email", email);
            $.ajax({
                type: "POST",
                url: '/upload-file',
                data: form_data,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                dataType: 'json',
                processData: false,  // tell jQuery not to process the data
                contentType: false,
                cache: false,
                beforeSend: function() {
                    $('.container-upload .box__uploading').removeClass('d-none');
                },
                success: function(data) {
                    $('.container-upload').addClass('d-none');
                    $('.confirmation').removeClass('d-none');

                    // $('.confirmation .file-name').text(data.filename.split(/[/ ]+/).pop());
                    $('.confirmation .file-name').text(data.filename);
                },
                complete: function() {
                    $('.container-upload .box__uploading').addClass('d-none');
                },
                error: function(data) {
                    $('.container-upload #error').text("Something went wrong. Please try again!");
                }
            }); 

            // Display confirmation message
        };
    }
})
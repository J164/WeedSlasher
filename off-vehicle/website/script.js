var imgInput;
function displayFile() {
    var display = document.getElementById('display');
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    var reader = new FileReader();

    reader.onloadend = function () {
        var img = document.createElement('img');
        img.src = reader.result;
        imgInput = reader.result;
        img.style.minWidth = '300px';
        img.style.maxWidth = '70%';
        display.innerHTML = '';
        display.appendChild(img);    
    };

    if (file) {
        reader.readAsDataURL(file);
    } else {
        display.innerHTML = 'No file selected';
    }
}
var canvas;
var ctx;
var isDrawing = false;
var startCoords, endCoords;
var selectedRegions = [];

    
        function displayRealNumber() {
            // Get user input value
            var inputHeight = document.getElementById('inputHeight').value;
            var inputWidth = document.getElementById('inputWidth').value;

            // Validate input using regex
            var regex = /^-?\d+(\.\d+)?$/;
            if (!regex.test(inputHeight)) {
                alert('Please enter a valid height.');
                return;
            }
            if (!regex.test(inputWidth)) {
                alert('Please enter a valid width.');
                return;
            }

            // Display user input
            var displayElement = document.getElementById('displayRealNumber');
            displayElement.innerHTML = '<p>Dimension: ' + inputHeight + ' x ' + inputWidth + '</p>';
            // var displayButton = document.getElementById('displayInfoButton');
            // //<label for="inputWidth">Enter a width(ft):</label>
            // //<input type="text" id="inputWidth" placeholder="Type here..." pattern="-?\d+(\.\d+)?" title="Please enter a valid width"></input>
            var main = document.getElementById('main');
            // infoButton = document.createElement('button');
            // infoLabel = document.createElement('label');
            // infoInput = document.createElement('input');

            // infoLabel.innerHTML = 'Enter 0 or 1';
            // infoInput.id = 'infoInput';
            // infoButton.onclick = 'saveInfo()';

            // displayButton.appendChild(infoLabel);
            // displayButton.appendChild(infoInput);
            // displayButton.appendChild(infoButton);


            var existingCanvas = document.getElementById('canvas');
            if (existingCanvas) {
                existingCanvas.parentNode.removeChild(existingCanvas);
            }
            
            canvas = document.createElement('canvas');
            ctx = canvas.getContext('2d');
            canvas.id = 'canvas';
            canvas.height = inputHeight;
            canvas.width = inputWidth;
            canvas.addEventListener('mousedown', handleMouseDown);
            canvas.addEventListener('mousemove', handleMouseMove);
            canvas.addEventListener('mouseup', handleMouseUp);
            canvas.style.border = '1px solid #000';
            canvas.style.margin = '50px';
            // Append the canvas to the body
            main.appendChild(canvas);
            
            var saveButton = document.getElementById('saveButton');
            var finishButton = document.getElementById('finishButton');
            var undoSaveButton = document.getElementById('undoSaveButton');
            saveButton.style.display = 'block';
            undoSaveButton.style.display = 'block';
            undoSaveButton.style.cursor = 'default';
            finishButton.style.display = 'block';
            
        }
        function undoSave() {
            if (selectedRegions.length > 0) {
                selectedRegions.pop();
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.strokeStyle = 'black';
                selectedRegions.forEach(function (region) {
                ctx.strokeRect(region.startX, region.startY, region.endX - region.startX, region.endY - region.startY);
                
            });

            } else {
                alert('Can\'t undo');
                return;
            }
            if (selectedRegions.length == 0) {
                undoSaveButton.style.opacity = '70%';
                undoSaveButton.style.cursor = 'default';
            }
        }
        // function saveInfo() {
        //     var info = document.getElementById('infoInput').value;
        //     selectedRegionInfos.push({info});
        // }
        function handleMouseDown(e) {
            isDrawing = true;
            startCoords = getMouseCoordinates(e);
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw all selected regions
            ctx.strokeStyle = 'black';
            selectedRegions.forEach(function (region) {
                ctx.strokeRect(region.startX, region.startY, region.endX - region.startX, region.endY - region.startY);
            });
        }

        function handleMouseMove(e) {
            if (!isDrawing) return;

            endCoords = getMouseCoordinates(e);
            
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = 'black';
            selectedRegions.forEach(function (region) {
                ctx.strokeRect(region.startX, region.startY, region.endX - region.startX, region.endY - region.startY);
            });

            // Clear the canvas and draw a rectangle
            ctx.strokeStyle = 'cornflowerblue';
            ctx.strokeRect(startCoords.x, startCoords.y, endCoords.x - startCoords.x, endCoords.y - startCoords.y);
        }
        function displayRegion() {
            selectedRegions.push({
                startX: startCoords.x,
                startY: startCoords.y,
                endX: endCoords.x,
                endY: endCoords.y
            });
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw all selected regions
            ctx.strokeStyle = 'black';
            selectedRegions.forEach(function (region) {
                ctx.strokeRect(region.startX, region.startY, region.endX - region.startX, region.endY - region.startY);
            });
            var undoSaveButton = document.getElementById('undoSaveButton');
            undoSaveButton.style.opacity = '100%';
            undoSaveButton.style.cursor = 'pointer';
        }   

        function handleMouseUp() {
            isDrawing = false;
            ctx.strokeStyle = 'black';
            selectedRegions.forEach(function (region) {
                ctx.strokeRect(region.startX, region.startY, region.endX - region.startX, region.endY - region.startY);
            });
            // Log or store the coordinates as needed
            console.log('Start Coordinates:', startCoords);
            console.log('End Coordinates:', endCoords);
            
        }

        function getMouseCoordinates(event) {
            var rect = canvas.getBoundingClientRect();
            return {
                x: event.clientX - rect.left,
                y: event.clientY - rect.top
            };
        }
        function sendData() {
            const c = JSON.stringify(selectedRegions);
            const p = JSON.stringify(imgInput);
            console.log(c);
            window.alert(c);
            // $.ajax({
            //     url:"http://127.0.0.1:5000/user/add",
            //     type:"POST",
            //     contentType: "application/json",
            //     data: JSON.stringify(c)
            // });
            var dataToSend = {
                key: c,
                anotherkey: p
            };

            // Make an AJAX POST request to Flask
            fetch('http://127.0.0.1:5000/receive_data', {
                mode: 'no-cors',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSend)
            })
            .then(() => {
                console.log('Success!');
            })
            .catch(error => {
                console.error('Error:', error);
            })
            if (selectedRegions.length > 0) {
                location.reload();
            }
            
            
        }
        // document.addEventListener('DOMContentLoaded', function () {
        //     // Sample data to send
        //     var dataToSend = {
        //         key: 'value',
        //         anotherKey: 'anotherValue'
        //     };

        //     // Make an AJAX POST request to Flask
        //     fetch('http://127.0.0.1:5000/receive_data', {
        //         mode: 'no-cors',
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/json'
        //         },
        //         body: JSON.stringify(dataToSend)
        //     })
        //     .then(() => {
        //         console.log('Success!');
        //     })
        //     .catch(error => {
        //         console.error('Error:', error);
        //     });
        // });
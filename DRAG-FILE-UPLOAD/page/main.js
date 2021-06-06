var file = document.querySelector("#getfile");

file.onchange = function(){
    
    var fileList = file.files;

    var reader = new FileReader();
    reader.readAsDataURL(fileList[0]);

    reader.onload = function (){
        document.querySelector("#preview").src = reader.result;

        var tempImage = new Image();
        tempImage.src = reader.result;
        tempImage.onload = function(){
            var canvas = document.createElement('canvas');
            var canvasContext = canvas.getContext("2d");

            canvas.width = 100;
            canvas.height = 100;

            canvasContext.drawImage(this,0,0,100,100);

            var dataURI = canvas.toDataURL("image/jpeg");

            document.querySelector("#thumbnail").src = dataURI;
            document.querySelector("#download").href = dataURI;
        }
    };
};
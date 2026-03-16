const input = document.getElementById("imageInput");
const preview = document.getElementById("preview");

input.addEventListener("change", function(){

const file = input.files[0];

if(file){
preview.src = URL.createObjectURL(file);
}

});

async function removeBG(){

const file = input.files[0];

if(!file){
alert("Upload image first");
return;
}

const formData = new FormData();
formData.append("image", file);

const loader = document.getElementById("loader");
loader.style.display="block";

const response = await fetch("/remove-bg",{
method:"POST",
body:formData
});

const blob = await response.blob();

const url = URL.createObjectURL(blob);

const result = document.getElementById("result");
result.src = url;

loader.style.display="none";
}

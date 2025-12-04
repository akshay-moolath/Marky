//render function connected to render button
async function render() 
{
    const inputBox = document.getElementById('inputBox');
    const previewBox = document.getElementById('preview-box');        
    const inputText = inputBox.value;
    const response = await fetch('/render', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
            body: new URLSearchParams({ 'md': inputText })
        });

        previewBox.innerHTML = await response.text();
        
                                    
}                                        



        
  //correcting text in the previw box      
        async function correctPreviewText() {
            const preview = document.getElementById("preview-box");
            const corrected = document.getElementById("corrected-box");
            const html = preview.innerHTML.trim();

            const response = await fetch("/correct", {
            method: "POST",
            headers: { "Content-Type": "text/plain"},
            body: html
            });
            const data = await response.json();
            corrected.innerHTML = data.corrected_html; 
            }
                

        
       
//downloading the preview text
function downloadCorrectedAsPdf() {
    const element = document.getElementById('corrected-box');
    const oldWidth = element.style.width;
    element.style.width = "800px"; 
    element.style.maxWidth = "none";

    const opt = {
        margin: 0.5,
        filename: 'corrected_document.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
        pagebreak: { mode: 'css' }
    };

    html2pdf().set(opt).from(element).save().then(() => {
        element.style.width = oldWidth;
        element.style.maxWidth = "";
    });
}    
   
    
    function clearText(){
            document.getElementById("inputBox").value = "";
            document.getElementById("preview-box").innerHTML = "";
        }

    async function uploadFileAndView(){
        const inputBox = document.getElementById('inputBox');
        const input = document.getElementById('fileInput');
        const file = input.files[0];
        const formData = new FormData();
        formData.append('file', file);


        const res = await fetch('/upload', {
      method: 'POST',
      body: formData });
      const data = await res.json();
      inputBox.innerHTML = data.html;
      
    }
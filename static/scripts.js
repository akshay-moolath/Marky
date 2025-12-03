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

        const rawHtmlText = await response.text();
        previewBox.innerHTML = rawHtmlText;
                                    
}                                        



        
  //correcting text in the previw box      
        async function correctPreviewText() {
            const preview = document.getElementById("preview-box");
            const html = preview.innerHTML.trim();

            const response = await fetch("/correct", {
            method: "POST",
            headers: { "Content-Type": "text/plain"},
            body: html
            });
            const data = await response.json();
            preview.innerHTML = data.corrected_html; 
            }
                

        
       
//downloading the preview text
        function downloadPreviewText(){
            const text = document.getElementById("preview-box").innerText.trim();
            const blob = new Blob([text], {type:"text/plain"});
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "html_preview.txt";
            document.body.appendChild(a);
            a.click();
            URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }        

    
     function clearText(){
            document.getElementById("inputBox").value = "";
            document.getElementById("preview-box").innerHTML = "";
        }
function clearText(){
            document.getElementById("md-area").value = "";
            document.getElementById("preview-box").innerHTML = "";
        }

        function downloadPreviewText(){
            const text = document.getElementById("preview-box").innerText.trim();
            if(!text){ alert("Nothing to download."); return; }

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

        async function correctPreviewText() {
            const preview = document.getElementById("preview-box");
            const html = preview.innerHTML.trim();
            if (!html) { alert("Nothing to correct."); return; }

            // show spinner and disable button
            const spinner = document.getElementById("spinner");
            const btn = document.getElementById("correct-btn");
            spinner.classList.remove("hidden");
            btn.disabled = true;
            btn.style.opacity = 0.7;

            try {
                const response = await fetch("/correct", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ html: html })
                });

                if (!response.ok) {
                    let msg = "Correction failed.";
                    try {
                        const err = await response.json();
                        msg = err.detail || JSON.stringify(err);
                    } catch(_) {}
                    alert(msg);
                    return;
                }

                const data = await response.json();

                // Server should return { corrected_html: "<p>...</p>" }
                if (data.corrected_html) {
                    preview.innerHTML = data.corrected_html;
                } else if (data.corrected_text) {
                    
                } else {
                    alert("No corrected content returned.");
                }
            } catch (err) {
                console.error(err);
                alert("Network or server error while correcting text.");
            } finally {
                spinner.classList.add("hidden");
                btn.disabled = false;
                btn.style.opacity = 1;
            }
        }
function gen(){
    let url = document.getElementById("url");
    if(url.value == ""){
        document.getElementById("sum").innerText = "No URL inputted :(";
    }else if(url.value.includes("https://www.youtube.com/watch") == false){
        document.getElementById("sum").innerText = "Not a valid URL :(";
    }else{
        let loadings = ["loading", "loading.", "loading..", "loading..."];
        let index = 0;
        let interval = setInterval(() => {
            document.getElementById("sum").innerText = loadings[index];
            index = (index+1)%4;
        }, 250)
        fetch("/summarize",{
            method: "POST",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify({"data":url.value})
        })

        .then(response=>{
            if(!response.ok){
                console.log("response not okay :(")
            }else{
                return response.json();
            }
        })

        .then(data=>{
            if(data.message == "euge"){
                clearInterval(interval);
                document.getElementById("sum").innerText = data.summary;
                url.value = "";
            }else{
                document.getElementById("sum").innerText = "error";
            }
        })

        .catch(error=>{
            document.getElementById("sum").innerText = error;
        })
    }
}
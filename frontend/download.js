async function postVideo(api_url, video_url) {
    let formData = new FormData();
    formData.append("url", video_url);
    try {
        response = await fetch(api_url+"/url", {
            method: 'post',
            body: formData,
        });

        const jsonBody = await response.json();
        console.log(jsonBody);
        id = jsonBody.id;
        return id;
    } catch (e) {
        console.error(e);
    }
}

async function getVideo(api_url, id){
    try {
        await fetch(api_url + "/download?id="+ String(id), {
            method: 'GET',
        })

        const blob = await response.blob();
        return blob;
    } catch (e) {
        console.error(e);
    }
}

async function main(video_url){
    const api_url = "http://localhost:5000";
    id = await postVideo(api_url, video_url);
    console.log("the id is = ", id);
    videoblob = await getVideo(api_url, id);

    const url = window.URL.createObjectURL(videoblob); // create a local URL for the file
    const a = document.createElement('a'); // create an anchor element
    a.href = url;
    a.download = 'filename.mp3'; // specify the file name
    document.body.appendChild(a); // append anchor to the document
    a.click(); // trigger the download
    a.remove(); // remove the anchor from the document
    window.URL.revokeObjectURL(url); // clean up the URL
}
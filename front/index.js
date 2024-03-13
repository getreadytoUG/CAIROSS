document.addEventListener("DOMContentLoaded", function () {
    detect_box = document.getElementById('detect_box');
    detect_url = 'http://localhost:8000/stream/';
    detect_box.src = detect_url;

    detect_box.style.width = "100%"

    function get_signal(){
        fetch('http://localhost:8000/signal')
            .then(response => {
                // 응답 객체를 받아서 JSON 형태로 파싱
                return response.json();
            })
            .then(data => {
                // 파싱된 데이터를 사용하여 원하는 작업 수행
                console.log(data)
                if (Object.keys(data).length !== 0) {
                    let box2Div = document.getElementById("box2");

                    // box2Div의 자식 요소가 존재하는지 확인하고, 존재한다면 모두 제거합니다.
                    while (box2Div.firstChild) {
                        box2Div.removeChild(box2Div.firstChild);
                    }
                    // data가 빈 딕셔너리인 경우에 실행됩니다.
                    get_person(data);
                }else{
                    let box2Div = document.getElementById("box2");

                    // box2Div의 자식 요소가 존재하는지 확인하고, 존재한다면 모두 제거합니다.
                    while (box2Div.firstChild) {
                        box2Div.removeChild(box2Div.firstChild);
                    }
                    // box2Div에 새로운 <div> 요소 추가
                    let noneImgDiv = document.createElement("div");
                    noneImgDiv.id = "NoneImgDiv";

                    // <img> 요소 생성
                    let noneImg = document.createElement("img");
                    noneImg.id = "NoneImg";
                    noneImg.src = "./src/None.png";
                    noneImg.alt = "데이터가 없습니다";

                    // noneImgDiv에 <img> 요소 추가
                    noneImgDiv.appendChild(noneImg);

                    // box2Div에 noneImgDiv 추가
                    box2Div.appendChild(noneImgDiv);
                    box2Div.style.display = 'flex'
                }
            })
            .catch(error => {
                // 에러 처리
                console.error('Fetch Error:', error);
            });
    }

    function get_person(data) {
        // 새로운 div 요소 생성
        let box2Div = document.getElementById("box2");
        box2Div.style.flexWrap = 'wrap'

        for (let i = 0; i < data.length; i++) {
            let imgContainer = document.createElement("div");
            imgContainer.style.width = "100%";
            imgContainer.style.height = "30%";
            imgContainer.style.background = `url(http://localhost:8000/get_person)`;
    
            let mid_x = `${data[i]['w']}px`;
            let mid_y = `${720 - data[i]['h'] + 100}px`;
    
            imgContainer.style.backgroundPosition = `${mid_x} ${mid_y}`;
            box2Div.appendChild(imgContainer);
        }
    }
    
    setInterval(get_signal, 400)

});

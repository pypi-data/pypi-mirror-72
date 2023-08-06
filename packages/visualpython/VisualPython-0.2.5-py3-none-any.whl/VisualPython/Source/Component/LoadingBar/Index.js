
define([

], 
function() {
    // 특정 작업이 렌더링이 지연 될 때 사용자에게 데이터 처리 중임을 보여주는 LoadingBar를 만드는 함수
    // LoadingBar는 프로젝트에서 없앨 수도 있고 다른 LoadingBar를 사용할 수 있다고 생각합니다.
    const RenderLoadingBar = (titleStr) =>{
        $(`<div class="loadingBar"></div>`)
            .load(Jupyter.notebook.base_url + "nbextensions/VisualPython/Source/Component/LoadingBar/Index.html", 
                (response, status, xhr) => {

            })
            .appendTo('.directoryComponent-container');
    }
    return RenderLoadingBar;
});


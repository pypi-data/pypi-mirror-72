define([

], 
function() {
    // 필요한 정보를 인자로 받아서 Alert 모달을 만드는 함수
    // FIXME: 현재 파일네비게이션 용으로만 만든 상태입니다.
    //        General하게 바꿔 사용해야 하는 모달입니다.
    const RenderAlertModal = (titleStr) =>{
        $(`<div class="alertModal"></div>`)
            .load(Jupyter.notebook.base_url + "nbextensions/VisualPython/Source/Component/AlertModal/Index.html", 
                (response, status, xhr) => {
                $('.alertModal-titleStr').html(titleStr);

                $('.alertModal-yes').click(() => {
                    $('.FileNavigationPage-inner').find('.alertModal').remove();
                });
            })
            .appendTo('.FileNavigationPage-inner');
    }
    return RenderAlertModal;
});

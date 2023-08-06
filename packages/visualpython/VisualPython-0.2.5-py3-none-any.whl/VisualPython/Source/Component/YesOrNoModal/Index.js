define([
    "nbextensions/VisualPython/Source/FrontEndApi/Index",
], 
function(
    FrontEndApis
) {
    const { SetCodeAndExecute,
            ExecuteAtJupyterKernelToDir } = FrontEndApis.JupyterNativeApi;
    // 필요한 정보를 인자로 받아서 YesOrNo 모달을 만드는 함수
    // FIXME: 현재 파일네비게이션 용으로만 만든 상태입니다.
    //        General하게 바꿔 사용해야 하는 모달입니다.
    const RenderYesOrNoModal = (dirPath, filePathStr, baseDirStr) =>{
        $(`<div></div>`)
            .load(Jupyter.notebook.base_url + "nbextensions/VisualPython/Source/Component/YesOrNoModal/Index.html", 
                 (response, status, xhr) => {
                    console.log("dirPath, filePathStr, baseDirStr",dirPath, filePathStr, baseDirStr);
                $(".yesOrNoModal-filePathStr").html(filePathStr);

                $('.yesOrNoModal-yes').click(() => {
                    const slashstr = `/`;
                    let executedString = `csv_data = pd.read_csv('${dirPath}${slashstr}${filePathStr}')\n`;
                                
                    if($(".isPrintedCSVData-checked:checkbox[name=isPrintedCSVData-checked]").is(":checked") === true) {
                        executedString += `csv_data`;
                    } 

                    ExecuteAtJupyterKernelToDir(baseDirStr, () => {
                        $('.directoryComponent-container').empty();
                        $('.FileNavigationPage-inner').find('.yesOrNoModal').remove();
                        $('.FileNavigationPage').addClass("hide");
                        $('.FileNavigationPage').removeClass("show");
                        $('.FileNavigationPage').css("display" ,"none");
                    });

                    SetCodeAndExecute(executedString);

                });

                $('.yesOrNoModal-no').click(() => {
                    $('.FileNavigationPage-inner').find('.yesOrNoModal').remove();
                });
            }).appendTo('.FileNavigationPage-inner');

    }

    return RenderYesOrNoModal;
});
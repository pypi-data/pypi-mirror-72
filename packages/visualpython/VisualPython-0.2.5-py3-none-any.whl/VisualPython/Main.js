
define([
    "require",
    "jquery",
    "base/js/namespace",
    "base/js/events",
    "codemirror/lib/codemirror",

    "nbextensions/VisualPython/Source/ConstData/ConstString/Index",
    "nbextensions/VisualPython/Source/GlobalModel/Index",
    "nbextensions/VisualPython/Source/Controller/Index",
    "nbextensions/VisualPython/Source/FrontEndApi/Index",
    "nbextensions/VisualPython/Source/Page/Index",
],  function(
    Requirejs,
    $,
    Jupyter,
    Events,
    Codemirror,

    ConstString,
    GlobalModels,
    Controllers,
    FrontEndApis,
    Pages
) {
    "use_strict";

    Jupyter.notebook.keyboard_manager.disable();
    const { STR_SCANDIR } = ConstString;
    const { MainController } = Controllers;
    const { SettingModel } = GlobalModels;
    const { MainPageController } = Pages;
    const { ExecuteAtJupyterKernelPwd } = FrontEndApis.JupyterNativeApi;
            
    $('<link rel="stylesheet" type="text/css">')
        .attr('href', Requirejs.toUrl('./StaticFile/CSS/Index.css'))
        .appendTo('head');

    $('<link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet"></link>')
        .appendTo('head');

    $('#site').css('position',"relative");

    $(`<div draggable="true" class="MainContainer-container ui-draggable ui-draggable-handle ui-resizable" style="display:none;"></div>`)
        .load(Jupyter.notebook.base_url + "nbextensions/VisualPython/MainLayout.html",  (response, status, xhr) => {
            if (status === "error") {
            //     alert(xhr.status + " " + xhr.statusText);
            }

            // 현재의 디렉토리 path str 정보를 전역 settingModel 클래스에 저장함
            ExecuteAtJupyterKernelPwd((currentDirStr) => {
                SettingModel.SetBaseDirStr(currentDirStr);
            });

            // VisualPython의 모든 page html을 렌더링하고 page마다 필요한 함수와 데이터를 init 한다.
            MainController.Init();
 
        })
        .appendTo('#site');

    Jupyter.toolbar.add_buttons_group([{
        label: 'Visual Python',
        icon: 'fa-text-width',
        callback: () => {
            MainPageController.ToggleIsShowMainDom();
        }
    }]);

});


define([

    "nbextensions/VisualPython/Source/FrontEndApi/Index",
], function( 
    FrontEndApis
 )
{
    const MainPageController = class {
        static mInstance = null;

        static mMainDom = null;
        static mMainDomBody = null;
        static mIsShowMainDom = false;
    
        constructor(){
            if(!this.mInstance){
                this.mInstance = this;
            } 
            return this.mInstance;
        }
        /* TODO: 비주얼 파이썬 html을 보였다 안 보였다하는 toggle함수 입니다.
                 현재는 css display를 통해 임시로 toggle기능을 만들었지만,
                 isShow 값을 사용자가 옵션에서 정하게 해서
                 다시 비주얼 파이썬을 켰을 때 화면이 보일지 안 보일지 결정하게 하는 것이 낫다고 생각합니다.
        */
        ToggleIsShowMainDom = () => {
            if(this.mIsShowMainDom === true){
                this.mMainDom.css("display" ,"none");
                this.mIsShowMainDom = false;
            } else {
                this.mMainDom.css("display" ,"flex");
                this.mIsShowMainDom = true;
            }
        }

        /* TODO: MainPageController는 다른 PageController의 상위 Controller입니다.
                 클래스 상속 개념이 은 아니지만, 비주얼 파이썬 전체 dom이나 태그, html을 조작할 수 있는 기능이 필요하다
                 해서 만들었습니다.

                 draggable()은 이동 가능하게하고 resizable() 사이즈를 줄이게 합니다.
                 ${bodyHeight - headerHeight}px은 비주얼 파이썬이 주피터 header를 제외하고 나머지 height를 다 차지합니다.

                 주피터 셀과 비주얼 파이썬을 화면 분할 시켜보는 뷰작업이 필요합니다.
        */
        Init = () => {
            console.log("MainPageController");

            this.mMainDom = $(".MainContainer-container");
            this.mMainDomBody = $(".MainContainer-body");
            $(".MainContainer-container").draggable();
            $(".MainContainer-container").resizable();

            const { GetDom, GetDomHeight } = FrontEndApis.DocumentObjectModelApi;
            const bodyHeight = GetDomHeight("body");
            const headerHeight = GetDomHeight("#header");
            GetDom(".MainContainer-container").style.height = `${bodyHeight - headerHeight}px`;
        }
    }
    
    return new MainPageController();  
})

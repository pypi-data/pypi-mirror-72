define([
    "nbextensions/VisualPython/Source/Page/Index",
    "nbextensions/VisualPython/Source/GlobalModel/Index",
    "nbextensions/VisualPython/Source/SystemData/Index",
],  function(
    PageControllers,
    GlobalModels,
    SystemData
) {
    
    // 1. Visual Python 시작시 new MainController()로 시스템 데이터, 페이지 컨트롤러, 글로벌 모델을 가져온다.
    // 2. 그런 다음 main.js가 MainController.Init을 실행한다.
    // 3. MainController.Init은 Visual Python에 존재하는 각 page의 html을 불러오거나 데이터를 가져오거나 함수를 지정된 page 태그에 맵핑시킨다
    
    const MainController = class {
        static mInstance = null;

        mSystemData;
        mUserData;

        mGlobalModelArr = [];
        mPageControllerObj = {};

        // 클래스는 싱글톤
        constructor(systemData, pageControllers, globalModels){
      
            if(!this.mInstance){
                this.mSystemData = systemData;
                this.mGlobalModelArr = Object.values(globalModels);
                this.mPageControllerObj =  pageControllers;
                this.mInstance = this;
            } 
            return this.mInstance;
        }

        static GetInstance = () => {
            return this;
        }

        // 각 페이지별로 존재하는 Controller를 init 시킵니다.
        // Controller들은 html을 렌더링하고 함수를 매핑시키거나 데이터를 model에 저장할 수 있습니다.
        Init = () => {
     
            const { MainPageController,
                    DashboardPageController,
                    PalettePageController,
                    MyTemplatePageController,
                    SettingPageController,
                    FileNavigationPageController } = this.mPageControllerObj;

            MainPageController.Init();
            DashboardPageController.Init();
            PalettePageController.Init(this.mSystemData);
            MyTemplatePageController.Init();
            SettingPageController.Init();
            FileNavigationPageController.Init();

        }
    }

    const mainController = new MainController(SystemData , PageControllers, GlobalModels)
    return mainController;
});

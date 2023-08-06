define([
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/Index`,
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
], function(
    PaletteElementMap,
    FrontEndApis,
)
{
    // 현재 js파일에서 사용할 api, config 값 불러옴
    const { MapOneArrayToDoubleArray } = FrontEndApis.ArrayApi;

    /* TODO: PalettePage는 사용자가 지정된 함수 등을 통해 주피터셀에서 필요한 작업을 도와주는 화면입니다.
             현재 임시로 Numpy, Pandas 단위를 PaletteBlock으로 보고
             그 아래로 Numpy의 np함수, Pandas의 pd함수를 PaletteElement로 보고 만들고 있습니다.

             현재 임시로 PalettePage가 만든 버튼을 누르면 코드가 셀에 실행됩니다.
             앞으로는 버튼을 누르면 기능 화면으로 들어가 변수 지정, 옵션 설정등을 통한 코드 generate 기능을 만들예정입니다.
    */
    const PalettePageController = class {
        static mInstance = null;

        mPalettePageSystemData = null;
        mPaletteElementMap = null;

        constructor(paletteElementMap){
            if(!this.mInstance){
                this.mInstance = this;
                this.mPaletteElementMap = paletteElementMap;
            } 
            return this.mInstance;
        }

        static GetInstance = () => {
            return this.mInstance;
        }

        /*
            SystemData의 PalettePage의 pageModel모델을 저장합니다.
            그리고 this.render() 렌더링을 합니다.
        */
        Init = (systemData) => {

            Object.values(systemData.pageList).some(data => {
                if(data.pagename === "PalettePage"){
                    this.mPalettePageSystemData =  data.pageModel;
                    return true;
                }
                return false;
            });

            this.render();
        }
        /* TODO:
            시스템 정보를 받아서 palette 버튼을 렌더링합니다.
            각 라이브러리마다 한 줄에 3개의 버튼이 있는 형태로 버튼을 나열했습니다.

            렌더링 형태는 언제든지 변할 수 있습니다.
        */
        render = () => {
            Object.entries(this.mPalettePageSystemData).forEach(data => {
                const paletteBlockTitle = data[0];
                const paletteBlock = this.makePaletteBlock(paletteBlockTitle);

                const paletteElements = Object.values(data[1]);
                const paletteElementDoubleArray = MapOneArrayToDoubleArray(paletteElements,paletteElements.length,3);

                this.makePaletteElement(paletteElementDoubleArray, paletteBlock);
            });
        }
        /* TODO:
            PaletteBlock을 만들면, 안에는 PaletteElement를 만듭니다.
            Palette 버튼을 누르면 각 기능 버튼마다 매핑해놓은 ExecuteCode함수가 실행되어 코드를 셀에 실행합니다.
            
            앞으로 개발하면서 하드코딩으로 매핑한 ExecuteCode가 아닌 함수 버튼별 화면 전환으로 바뀔 예정입니다.
            그리고 바뀐 화면에서 사용자가 
        */
        makePaletteElement = (paletteElementDoubleArray, paletteBlock) => {
            paletteElementDoubleArray.forEach((paletteElements) => {
                const blockBody = $(`<div class="PalettePage-block-body">
                                    </div>`);
                paletteElements.forEach((element) => {
                    $(`<input class="${element.cssClassName}" id="Base-input-button" type="submit" value="${element.tagValue}" />`)
                        .appendTo(blockBody).click(() => {
                            this.mPaletteElementMap.get(element.name).ExecuteCode();
                        });   
                       
                });
                blockBody.appendTo(paletteBlock);
            });
            paletteBlock.appendTo('.PalettePage-container');
        }
        /* TODO:
                PaletteBlock을 만듭니다.
                PaletteBlock이 Numpy, Pandas 기능을 담는 컨테이너이면
                안에 PaletteElement(np.arrange,pd.merge 함수)를 append해서 렌더링합니다.
        */
        makePaletteBlock = (blockTitleStr) => {
            const paletteBlock = $(`<div class="PalettePage-block">
                                        <div class="PalettePage-block-title">
                                            ${blockTitleStr}
                                        </div>
                                    </div>`);
            return paletteBlock;
        }
    }

    return new PalettePageController(PaletteElementMap);
})
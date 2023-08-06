define([
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/BaseLibrary/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/Csv/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/Numpy/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/Pandas/Index`,
], function(
    BaseLibrary,
    Csv,
    Numpy,
    Pandas
)
{
    /* TODO:
        PaletteElement들을 해쉬 맵으로 저장합니다. Map 객체는 최신자바스크립트 객체입니다.
        키는 name
        밸류는 각 PaletteElement 클래스입니다.

        name은 PaletteElement 클래스마다 지정되어 있고, 이들은 SystemData에 저장된 name과 같습니다.
        name을 통해 특정 PaletteElement 클래스를 불러올 수 있습니다.
        
        코드를 만드는 함수, 기능 모듈 등을 관리하는 방식은 여러가지가 있어 이 구조는 언제든 바뀔 수 있습니다.
    */
    const PaletteElementMap = new Map();
    PaletteElementMap.set(BaseLibrary.GetName(), BaseLibrary);
    PaletteElementMap.set(Csv.GetName(), Csv);

    Object.values(Numpy).forEach((paletteElement) => {
        const name = paletteElement.GetName();
        PaletteElementMap.set(name,paletteElement);
    });

    Object.values(Pandas).forEach((paletteElement) => {
        const name = paletteElement.GetName();
        PaletteElementMap.set(name,paletteElement);
    });

    return PaletteElementMap;
});

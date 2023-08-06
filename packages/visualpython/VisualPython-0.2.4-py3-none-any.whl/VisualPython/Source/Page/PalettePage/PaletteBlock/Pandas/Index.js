define([
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/Pandas/PdDataFrame/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/Pandas/PdDaterange/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/Pandas/PdMap/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/Pandas/PdMerge/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/Pandas/PdSeries/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/Pandas/PdConcat/Index`,
], function(
    PdDataFrame,
    PdDaterange,
    PdMap,
    PdMerge,
    PdSeries,
    PdConcat
)
{
    return {
        PdDataFrame,
        PdDaterange,
        PdMap,
        PdMerge,
        PdSeries,
        PdConcat
    }
});

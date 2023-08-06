define([
    "./MainPageController",
    "./DashboardPage/Controller",
    "./PalettePage/Controller",
    "./MyTemplatePage/Controller",
    "./SettingPage/Controller",
    "./FileNavigationPage/Controller"
], function(
    MainPageController,
    DashboardPageController,
    PalettePageController,
    MyTemplatePageController,
    SettingPageController,
    FileNavigationPageController
) {

    return {
        MainPageController,
        DashboardPageController,
        PalettePageController,
        MyTemplatePageController,
        SettingPageController,
        FileNavigationPageController
    }
});

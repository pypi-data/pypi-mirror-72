define([
    "./LoadingBar/Index",
    "./AlertModal/Index",
    "./YesOrNoModal/Index"
], 
function(
    RenderLoadingBar,
    RenderAlertModal,
    RenderYesOrNoModal
) {
    return {
        RenderLoadingBar,
        RenderAlertModal,
        RenderYesOrNoModal
    }
});
define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const NpZeros = class extends PaletteElement {
        static mInstance = null;
        mName = "NpZeros";
        
        constructor(){
            super();
            if(!this.mInstance){
                this.mInstance = this;
            } 
            return this.mInstance;
        }

        static GetInstance = () => {
            return this.mInstance;
        }

        GetName = () => {
            return this.mName;
        }

        ExecuteCode = () => {
            let str = `arr1 = np.zeros(202)\n`;
            str += `print(arr1)\n`;
            str += `arr2 = np.zeros((20,30))\n`;
            str += `print(arr2)`;

            SetCodeAndExecute(str);
        }
    }
    
    return new NpZeros();
});
